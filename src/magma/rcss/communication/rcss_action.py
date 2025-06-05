from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from magma.agent.communication.action import Effector

if TYPE_CHECKING:
    from magma.common.math.geometry.pose import Pose2D


@dataclass(frozen=True)
class CreateEffector(Effector):
    """Effector for creating an robot scene instance within the simulation."""

    scene: str
    """The target scene."""

    model_type: int
    """The model type."""


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


@dataclass(frozen=True)
class SayEffector(Effector):
    """Effector for audio output within the simulation."""

    message: str
    """The message to say."""


@dataclass(frozen=True)
class PassModeEffector(Effector):
    """Effector for requesting a pass mode for our team within the simulation."""
