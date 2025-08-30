from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from magmapy.agent.communication.action import Effector

if TYPE_CHECKING:
    from magmapy.common.math.geometry.pose import Pose2D


@dataclass(frozen=True)
class InitEffector(Effector):
    """Effector for initializing a player instance within the simulation."""

    team_name: str
    """The own team name."""

    player_no: int
    """The own player number."""

    model_name: str
    """The name of the robot model to load for the agent.

    Note: Not used for SimSpark.
    """


@dataclass(frozen=True)
class SyncEffector(Effector):
    """Effector for synchronizing with the simulation."""


@dataclass(frozen=True)
class BeamEffector(Effector):
    """Effector for beaming within the simulation."""

    beam_pose: Pose2D
    """The beam target pose."""
