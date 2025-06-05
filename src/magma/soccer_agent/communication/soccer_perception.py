from dataclasses import dataclass

from magma.agent.communication.perception import Perceptor


@dataclass(frozen=True)
class SoccerGameStatePerceptor(Perceptor):
    """Perceptor representing a soccer game state."""

    play_time: float
    """The current play time."""

    play_side: str
    """The current play side."""

    play_mode: str
    """The current play mode."""

    player_no: int
    """The player number."""

    score_left: int
    """The left team score."""

    score_right: int
    """The right team score."""
