from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from magmapy.agent.model.robot.actuators import Actuator
from magmapy.common.math.geometry.pose import P2D_ZERO
from magmapy.common.math.geometry.vector import V3D_ZERO, Vector3D
from magmapy.rchl.communication.rchl_action import RCHLTeamComEffector
from magmapy.rchl.communication.rchl_mitecom import RCHLTeamMessage, RCHLTeamRobot

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magmapy.agent.communication.action import Action
    from magmapy.common.math.geometry.pose import Pose2D


@runtime_checkable
class PRCHLTeamComActuator(Protocol):
    """Protocol for team communication actuators."""

    def set(
        self,
        player_no: int,
        own_pose: Pose2D,
        target_pose: Pose2D,
        ball_pos: Vector3D,
        players: Sequence[tuple[bool, Pose2D]],
    ) -> None:
        """Set the team communication action.

        Parameter
        ---------
        player_no : int
            Our player number.

        own_pose : Pose2D
            Our (own) current pose.

        target_pose : Pose2D
            Our (own) target pose.

        ball_pos : Vector3D
            The ball position.

        players : Sequence[tuple[bool, Pose2D]]
            A list of team-indicators and player poses of the other players on the field.
        """


class RCHLTeamComActuator(Actuator):
    """Default init actuator implementation."""

    def __init__(self, name: str, effector_name: str) -> None:
        """Create a new init actuator.

        Parameter
        ---------
        name : str
            The unique actuator name.

        effector_name : str
            The name of the effector associated with this actuator.

        model_name : str, default=''
            The name of the robot model to use.
        """

        super().__init__(name, effector_name)

        self._player_no: int = -1
        """The player number."""

        self._own_pose: Pose2D = P2D_ZERO
        """Our (own) current pose."""

        self._target_pose: Pose2D = P2D_ZERO
        """Our (own) current pose."""

        self._ball_pos: Vector3D = V3D_ZERO
        """The ball position."""

        self._players: Sequence[tuple[bool, Pose2D]]
        """The list of team-indicators and player poses of the other players on the field."""

    def set(
        self,
        player_no: int,
        own_pose: Pose2D,
        target_pose: Pose2D,
        ball_pos: Vector3D,
        players: Sequence[tuple[bool, Pose2D]],
    ) -> None:
        """Set the team communication action.

        Parameter
        ---------
        player_no : int
            Our player number.

        own_pose : Pose2D
            Our (own) current pose.

        target_pose : Pose2D
            Our (own) target pose.

        ball_pos : Vector3D
            The ball position.

        players : Sequence[tuple[bool, Pose2D]]
            A list of team-indicators and player poses of the other players on the field.
        """

        self._player_no = player_no
        self._own_pose = own_pose
        self._target_pose = target_pose
        self._ball_pos = ball_pos
        self._players = players

    def commit(self, action: Action) -> None:
        if self._player_no > 0:
            players: Sequence[RCHLTeamRobot] = [RCHLTeamRobot(own_team, pose) for own_team, pose in self._players]
            msg = RCHLTeamMessage(self._player_no, self._own_pose, self._target_pose, self._ball_pos, players)
            action.put(RCHLTeamComEffector(self.effector_name, msg))

        # reset actuator
        self._player_no = -1
