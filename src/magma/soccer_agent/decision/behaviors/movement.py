from collections.abc import Mapping
from typing import Final

from magma.agent.decision.behavior import BehaviorID, PBehavior, PMoveBehavior, SingleComplexBehavior
from magma.common.math.geometry.angle import angle_to
from magma.common.math.geometry.pose import Pose2D
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D
from magma.soccer_agent.decision.soccer_behaviors import SoccerBehaviorID
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


class MoveToBehavior(SingleComplexBehavior):
    """Default move-to behavior for moving towards a desired 2D pose within the soccer world."""

    def __init__(self, model: PSoccerAgentModel, behaviors: Mapping[str, PBehavior]) -> None:
        """Create a new move-to behavior.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.
        """

        super().__init__(SoccerBehaviorID.MOVE_TO.value, behaviors)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        self._target_pose: Pose2D = Pose2D()
        """The global target pose to move to."""

        behavior = behaviors[BehaviorID.MOVE.value]
        self.move_behavior: Final[PMoveBehavior | None] = behavior if isinstance(behavior, PMoveBehavior) else None
        """The move behavior used to bring the agent to the desired position."""

        self.omni_movement_distance: Final[float] = 2.0
        """The distance to the target position below which to move omni-directional."""

    def set(self, target_pose: Pose2D) -> None:
        """Set the desired target pose to move to.

        Parameter
        ---------
        target_pose : Pose2D
            The global target pose.
        """

        self._target_pose = target_pose

    def _decide_next(self) -> PBehavior | None:
        if self.move_behavior is None:
            # no move behavior available --> can't to anything to move to the target pose
            return None

        forwards = 0.0
        sidewards = 0.0
        turn = 0.0

        own_pose = self.model.get_world().get_this_player().get_pose_2d()
        rel_target_pose = own_pose.inv_tf_pose(self._target_pose)
        target_distance = own_pose.pos.norm()

        if target_distance > self.omni_movement_distance:
            # turn and move straight towards the target position
            target_angle = angle_to(rel_target_pose.pos)

            if abs(target_angle.deg()) > 20:
                # more than 20 degrees deviation from the direction to the target position --> only turning towards target
                forwards = 0.0
                sidewards = 0.0
                turn = target_angle.deg()
            else:
                # facing the target position --> move towards the target and correct remaining directional deviation while moving forward
                forwards = rel_target_pose.x()
                sidewards = 0.0
                turn = target_angle.deg() * 0.25

        else:
            # omni-directional movement towards the target pose
            forwards = rel_target_pose.x()
            sidewards = rel_target_pose.y()
            turn = rel_target_pose.theta.deg()

        # forward new velocity parameter to move behavior
        self.move_behavior.set(Vector3D(forwards, sidewards, turn))

        return self.move_behavior


class MoveAlongBehavior(SingleComplexBehavior):
    """Default move-along behavior for moving along a desired 2D trajectory within the soccer world."""

    def __init__(self, model: PSoccerAgentModel, behaviors: Mapping[str, PBehavior]) -> None:
        """Create a new move-along behavior.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.
        """

        super().__init__(SoccerBehaviorID.MOVE_ALONG.value, behaviors)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        self._target_trajectory: list[Pose2D] = []
        """The global target trajectory to move along."""

        behavior = behaviors[BehaviorID.MOVE.value]
        self.move_behavior: Final[PMoveBehavior | None] = behavior if isinstance(behavior, PMoveBehavior) else None
        """The move behavior used to move the agent along the desired trajectory."""

    def set(self, target_trajectory: list[Pose2D]) -> None:
        """Set the desired target trajectory to move along.

        Parameter
        ---------
        target_trajectory : list[Pose2D]
            The global target trajectory.
        """

        self._target_trajectory = target_trajectory

    def _decide_next(self) -> PBehavior | None:
        if self.move_behavior is None:
            # no move behavior available --> can't to anything to move along the target trajectory
            return None

        if not self._target_trajectory:
            # no target(s) given --> don't move
            self.move_behavior.set(V3D_ZERO)
            return self.move_behavior

        forwards = 0.0
        sidewards = 0.0
        turn = 0.0

        own_pose = self.model.get_world().get_this_player().get_pose_2d()
        rel_target_pose = own_pose.inv_tf_pose(self._target_trajectory[0])

        # omni-directional movement towards the next target pose
        forwards = rel_target_pose.x()
        sidewards = rel_target_pose.y()
        turn = rel_target_pose.theta.deg()

        # forward new velocity parameter to move behavior
        self.move_behavior.set(Vector3D(forwards, sidewards, turn))

        return self.move_behavior
