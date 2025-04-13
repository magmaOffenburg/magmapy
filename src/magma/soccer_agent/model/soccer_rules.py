from __future__ import annotations


class SoccerRules:
    """
    Class for representing soccer specific rules.
    """

    def __init__(self,
                 match_duration: float,
                 match_overtime: float,
                 kick_off_time: float,
                 throw_in_time: float) -> None:
        """
        Create a new rule book.
        """

        self._duration: float = match_duration
        self._overtime: float = match_overtime
        self._kick_off_time: float = kick_off_time
        self._throw_in_time: float = throw_in_time

    def get_duration(self) -> float:
        """
        Retrieve the total duration of a normal soccer game.
        """

        return self._duration

    def get_overtime(self) -> float:
        """
        Retrieve the total overtime of a extended soccer game.
        """

        return self._overtime

    def get_kick_off_time(self) -> float:
        """
        Retrieve the time a team has to perform a kick-off before the game continues normally and the other team is allowed to approach the ball again.
        """

        return self._kick_off_time

    def get_throw_in_time(self) -> float:
        """
        Retrieve the time a team has to perform a throw-in before the game continues normally and the other team is allowed to approach the ball again.
        """

        return self._throw_in_time
