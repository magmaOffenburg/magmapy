from collections.abc import Sequence
from dataclasses import dataclass

from magmapy.common.math.geometry.pose import Pose2D
from magmapy.common.math.geometry.vector import Vector3D


@dataclass(frozen=True)
class RCHLTeamRobot:
    """Perceptor representing a RCHL team message."""

    own_team: bool
    """``True`` if the player is in our team, ``False`` if not."""

    pose: Pose2D
    """The pose of the robot."""


@dataclass(frozen=True)
class RCHLTeamMessage:
    """Message for RCHL team communication."""

    player_no: int
    """The player number."""

    pose: Pose2D
    """The current pose of the robot."""

    target_pose: Pose2D
    """The target pose of the robot."""

    ball: Vector3D
    """The position of the ball."""

    players: Sequence[RCHLTeamRobot]
    """The list of other players."""
