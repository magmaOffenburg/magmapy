from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final, cast

from magmapy.agent.decision.behavior import ComplexBehavior, PBehavior
from magmapy.common.math.geometry.angle import angle_to
from magmapy.common.math.geometry.pose import Pose2D
from magmapy.common.math.geometry.vector import Vector2D
from magmapy.soccer_agent.decision.soccer_behaviors import PKickBehavior, PMoveToBehavior, SoccerBehaviorID
from magmapy.soccer_agent.model.soccer_agent import PSoccerAgentModel


@dataclass
class KickOption:
    """Helper class for holding a kick option with evaluation results."""

    def __init__(self, kick: PKickBehavior) -> None:
        """Construct a new kick option."""

        self.applicability: float = -1.0
        """The applicability of the kick in the current situation."""

        self.executability: float = -1.0
        """The executability of the kick in the current situation."""

        self.kick: Final[PKickBehavior] = kick
        """The kick behavior."""

    def evaluate(self, target_position: Vector2D, *, is_goal_kick: bool = False) -> None:
        """Evaluate this kick for the given target position."""

        self.kick.set(target_position, is_goal_kick=is_goal_kick)

        self.applicability = self.kick.get_applicability()
        self.executability = -1.0 if self.applicability < 0 else self.kick.get_executability()


class Attack(ComplexBehavior):
    """Base implementation for positioning behaviors."""

    def __init__(
        self,
        model: PSoccerAgentModel,
        behaviors: Mapping[str, PBehavior],
        kick_behaviors: Sequence[str],
        *,
        name: str = SoccerBehaviorID.ATTACK.value,
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

        kick_behaviors : Sequence[str]
            The list of kick behavior names the attack behavior is based on.
        """

        super().__init__(name, behaviors)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        behavior = behaviors[SoccerBehaviorID.MOVE_TO.value]
        self.move_to_behavior: Final[PMoveToBehavior | None] = behavior if isinstance(behavior, PMoveToBehavior) else None
        """The move behavior used to maneuver the agent towards the preferred kick position."""

        self.kick_options: Final[list[KickOption]] = [KickOption(cast(PKickBehavior, behaviors[name])) for name in kick_behaviors if isinstance(behaviors[name], PKickBehavior)]
        """The list of kick options available to this attack behavior."""

        self._intended_kick_pos: Vector2D = self.model.get_world().get_map().get_opponent_goal_position().as_2d() + Vector2D(0, -1.05)
        """The intended kick position."""

    def _decide(self) -> Sequence[PBehavior]:
        if self.move_to_behavior is None:
            # no move-to behavior available --> can't move towards the ball
            return []

        # evaluate kick options
        self._evaluate_kick_options()

        # check if one or more kicks are executable in the current situation and - in case - decide for them
        executable_kicks = [opt.kick for opt in self.kick_options if opt.executability >= 0]
        if executable_kicks:
            return executable_kicks

        # move towards the best suiting applicable kick option
        kick_pose = self._get_preferred_move_to_pose()
        self.move_to_behavior.set(kick_pose)
        return [self.move_to_behavior]

    def _evaluate_kick_options(self) -> None:
        """Evaluate applicability and executability of available kick options."""

        for kick_option in self.kick_options:
            kick_option.evaluate(self._intended_kick_pos, is_goal_kick=False)

        self.kick_options.sort(key=lambda entry: (entry.applicability, entry.executability))

    def _get_preferred_move_to_pose(self) -> Pose2D:
        """Return the 2D pose on the field to which we need to move in order to perform the highest applicable kick."""

        if len(self.kick_options) > 0:
            ball_pos = self.model.get_world().get_ball().get_position().as_2d()
            ball_pose = Pose2D(ball_pos, angle_to(self._intended_kick_pos - ball_pos))

            return ball_pose.tf_pose(self.kick_options[0].kick.get_relative_move_to_pose())

        # no kick options --> no information where to move
        # TODO: Still walk behind the ball, facing the opponent goal
        return self.model.get_world().get_this_player().get_pose_2d()
