from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from magma.agent.decision.behavior import BehaviorID, PBehavior, PMoveBehavior, SingleComplexBehavior
from magma.common.math.geometry.angle import Angle2D, angle_to
from magma.common.math.geometry.bounding_box import AABB2D
from magma.common.math.geometry.pose import Pose2D
from magma.common.math.geometry.vector import V2D_ZERO, Vector2D, Vector3D
from magma.soccer_agent.decision.soccer_behaviors import SoccerBehaviorID
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


@dataclass(frozen=True)
class KickParameter:
    """Class representing a parameter set for a kick behavior.

    Most kick parameter are specified in a coordinate system with the ball as its origin facing the intended kick direction.
    """

    relative_move_to_pose: Pose2D
    """The target pose to move to when preparing for the kick."""

    kickable_area: AABB2D
    """The kickable area."""

    theta_range: Angle2D
    """The maximum allowed angular deviation from the desired kick direction this kick is able to handle."""


class WalkKick(SingleComplexBehavior):
    """Simple walk-kick, utilizing the movement platform to walk against the ball."""

    def __init__(
        self,
        model: PSoccerAgentModel,
        behaviors: Mapping[str, PBehavior],
        kick_parameter: KickParameter,
        name: str = SoccerBehaviorID.DRIBBLE.value,
    ) -> None:
        """Construct a new walk-kick.

        Parameter
        ---------
        kick_parameter : KickParameter
            The walk kick parameter set.
        """

        super().__init__(name, behaviors)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        self.kick_parameter: Final[KickParameter] = kick_parameter
        """The kick parameter set."""

        behavior = behaviors[BehaviorID.MOVE.value]
        self.move_behavior: Final[PMoveBehavior | None] = behavior if isinstance(behavior, PMoveBehavior) else None
        """The move behavior used to dribble the ball."""

        self._target_position: Vector2D = V2D_ZERO
        """The kick target position."""

        self._is_goal_kick: bool = False
        """Flag indicating if the performed kick is a goal kick."""

    def get_params(self) -> KickParameter:
        """Return the kick parameter set of this kick."""

        return self.kick_parameter

    def set(self, target_position: Vector2D, *, is_goal_kick: bool = False) -> None:
        """Set the desired target position to kick.

        Parameter
        ---------
        target_position : Vector2D
            The global target kick position.

        is_goal_kick : bool, default=False
            Flag indicating if the intended kick is a goal kick.
        """

        self._target_position = target_position
        self._is_goal_kick = is_goal_kick

    def get_relative_move_to_pose(self) -> Pose2D:
        """Return the move-to pose relative to the ball and intended kick direction in order to perform this kick."""

        return self.kick_parameter.relative_move_to_pose

    def get_applicability(self) -> float:
        """Return the applicability of the kick.

        Returns
        -------
        utility : float
            **Negative values** indicate that the kick is not applicable in the current game situation.
            A **positive value** indicates that the kick in general is applicable in the current game situation and represent a measurement of how well it fits the requested kick.
        """

        return 1

    def get_executability(self) -> float:
        """Return the executability of the kick.

        Returns
        -------
        utility : float
            **Negative values** indicate that performing the kick is expected to **not hit the ball** and should therefore not be performed.
            A **positive value** indicates that the kick **should be able to hit the ball** and represents a measurement of how well it fits the kick (0 = worst; 1 = optimal).
        """

        # fetch ball position
        ball_pos = self.model.get_world().get_ball().get_position().as_2d()

        # check angle deviation
        intended_kick_direction = angle_to(self._target_position - ball_pos)
        own_direction = self.model.get_world().get_this_player().get_horizontal_angle()
        direction_deviation = intended_kick_direction - own_direction
        if abs(direction_deviation.rad()) > self.kick_parameter.theta_range.rad():
            return -1

        # check if ball is in kickable area
        local_ball_pos = self.model.get_world().get_this_player().get_pose_2d().inv_tf_vec(ball_pos)

        return 1 if self.kick_parameter.kickable_area.contains(local_ball_pos) else -1

    def _decide_next(self) -> PBehavior | None:
        if self.move_behavior is None:
            # no move behavior available --> can't dribble the ball
            return None

        if self._is_goal_kick:
            self.move_behavior.set(Vector3D(0.5, 0, 0))
        else:
            intended_kick_distance = (self._target_position - self.model.get_world().get_ball().get_position().as_2d()).norm()

            if intended_kick_distance < 1:
                self.move_behavior.set(Vector3D(0.25, 0, 0))
            else:
                self.move_behavior.set(Vector3D(0.5, 0, 0))

        return self.move_behavior
