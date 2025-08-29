from __future__ import annotations

from typing import Final


class SoccerRules:
    """Class for representing soccer specific rules."""

    def __init__(
        self,
        match_duration: float,
        match_overtime: float,
        kick_off_time: float,
        throw_in_time: float,
    ) -> None:
        """Create a new rule book."""

        self.duration: Final[float] = match_duration
        """The total duration of a normal soccer game."""

        self.overtime: Final[float] = match_overtime
        """The total overtime of an extended soccer game."""

        self.kick_off_time: Final[float] = kick_off_time
        """The time a team has to perform a kick-off before the game continues normally and the other team is allowed to approach the ball again."""

        self.throw_in_time: Final[float] = throw_in_time
        """The time a team has to perform a throw-in before the game continues normally and the other team is allowed to approach the ball again."""
