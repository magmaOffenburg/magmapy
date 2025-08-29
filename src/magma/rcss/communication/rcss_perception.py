from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from magma.agent.communication.perception import Perceptor, VisionPerceptor

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magma.common.math.geometry.vector import Vector3D


@dataclass(frozen=True)
class RCSSSMJGameStatePerceptor(Perceptor):
    """Perceptor representing game state information used in RoboCup Soccer Simulation (MuJoCo)."""

    play_time: float
    """The current play time."""

    play_mode: str
    """The current play mode."""

    left_team: str
    """The name of the left team."""

    right_team: str
    """The name of the right team."""

    score_left: int
    """The left team score."""

    score_right: int
    """The right team score."""


@dataclass(frozen=True)
class RCSSLineDetection:
    """A line object detection."""

    position1: Vector3D
    """The start position of the detected line in the camera local frame."""

    position2: Vector3D
    """The end position of the detected line in the camera local frame."""


@dataclass(frozen=True)
class RCSSPlayerDetection:
    """A player object detection."""

    team_name: str
    """The detected team of the player."""

    player_no: int
    """The detected player number."""

    body_parts: Sequence[tuple[str, Vector3D]]
    """The list of detected body parts of the player."""


@dataclass(frozen=True)
class RCSSVisionPerceptor(VisionPerceptor):
    """Perceptor representing a vision detection in the RoboCup Soccer Simulation."""

    lines: Sequence[RCSSLineDetection]
    """The collection of line detections."""

    players: Sequence[RCSSPlayerDetection]
    """The collection of player detections."""
