from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Final

from magma.agent.decision.behavior import BehaviorID, PBehavior, SingleComplexBehavior
from magma.common.math.geometry.angle import ANGLE_ZERO, Angle2D, angle_deg
from magma.common.math.geometry.pose import Pose2D
from magma.common.math.geometry.vector import V2D_ZERO, Vector2D
from magma.soccer_agent.decision.soccer_behaviors import PMoveToBehavior, SoccerBehaviorID
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel
from magma.soccer_agent.model.soccer_beliefs import AmIAtPosition, AmIFacingDirection


class PositioningBehavior(SingleComplexBehavior, ABC):
    """Base implementation for positioning behaviors."""

    def __init__(
        self,
        name: str,
        model: PSoccerAgentModel,
        behaviors: Mapping[str, PBehavior],
        lower_pd: float = 0.05,
        upper_pd: float = 0.2,
        lower_ad: Angle2D | None = None,
        upper_ad: Angle2D | None = None,
    ):
        """Create a new positioning behavior.

        Parameter
        ---------
        name : str
            The unique name of the behavior.

        model : PSoccerAgentModel
            The soccer agent model.

        behaviors : Mapping[str, PBehavior]
            The map of known behaviors.

        lower_pd : float, default=0.05
            The lower bound of position deviation hysteresis function.

        upper_pd : float, default=0.2
            The upper bound of position deviation hysteresis function.

        lower_ad : Angle2D | None, default=None
            The lower bound of direction deviation hysteresis function.
            If ``None``, a lower bound of 10 degrees is used by default.

        upper_ad : Angle2D | None, default=None
            The lower bound of direction deviation hysteresis function.
            If ``None``, an upper bound of 20 degrees is used by default.
        """

        super().__init__(name, behaviors)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        self.is_at_position: Final[AmIAtPosition] = AmIAtPosition(model, V2D_ZERO, lower_pd, upper_pd)
        """Belief for checking if the target position has been reached."""

        self.is_facing_direction: Final[AmIFacingDirection] = AmIFacingDirection(
            model,
            ANGLE_ZERO,
            angle_deg(10) if lower_ad is None else lower_ad,
            angle_deg(20) if upper_ad is None else upper_ad,
        )
        """Belief for checking if the target direction has been reached."""

        move_to_behavior = behaviors[SoccerBehaviorID.MOVE_TO.value]
        self._move_to_behavior: PMoveToBehavior | None = move_to_behavior if isinstance(move_to_behavior, PMoveToBehavior) else None
        """The move-to behavior used to move to the desired pose."""

    def _decide_next(self) -> PBehavior | None:
        if self._move_to_behavior is None:
            # no move-to behavior available --> can't to anything to move to the target position
            return None

        # check if target pose has been reached
        target_pose = self._get_target_pose()
        self.is_at_position.target_position = target_pose.pos
        self.is_facing_direction.target_direction = target_pose.theta
        self.is_at_position.update()
        self.is_facing_direction.update()

        if self.is_at_position and self.is_facing_direction:
            # the target pose is considered to be reached
            return self.behaviors[BehaviorID.GET_READY.value]

        # move towards the desired target pose
        self._move_to_behavior.set(target_pose)
        return self._move_to_behavior

    @abstractmethod
    def _get_target_pose(self) -> Pose2D:
        """Return the positioning target pose."""


class PenaltyPositioningBehavior(PositioningBehavior):
    """Penalty positioning behavior."""

    def __init__(self, model: PSoccerAgentModel, behaviors: Mapping[str, PBehavior]) -> None:
        """Construct a new penalty positioning behavior.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.

        behaviors : Mapping[str, PBehavior]
            The map of known behaviors.
        """

        super().__init__(
            SoccerBehaviorID.PENALTY_POSITIONING.value,
            model,
            behaviors,
            0.1,
            0.3,
            angle_deg(15),
            angle_deg(30),
        )

    def _get_target_pose(self) -> Pose2D:
        goal_rel_pose = Pose2D(Vector2D(-4, 1.3), angle_deg(-20))

        return Pose2D(self.model.get_world().get_map().get_opponent_goal_position().as_2d() - goal_rel_pose.pos, goal_rel_pose.theta)


class RolePositioningBehavior(PositioningBehavior):
    """Role-specific positioning behavior."""

    def __init__(self, model: PSoccerAgentModel, behaviors: Mapping[str, PBehavior]) -> None:
        """Construct a new role-specific positioning behavior.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.

        behaviors : Mapping[str, PBehavior]
            The map of known behaviors.
        """

        super().__init__(
            SoccerBehaviorID.ROLE_POSITIONING.value,
            model,
            behaviors,
            0.1,
            0.3,
            angle_deg(10),
            angle_deg(20),
        )

    def _get_target_pose(self) -> Pose2D:
        role = self.model.get_role_manager().get_role()

        if role is None:
            # no role --> stay where we are
            return self.model.get_world().get_this_player().get_pose_2d()

        return role.get_target_pose()
