from __future__ import annotations

from magma.soccer_agent.model.soccer_rules import SoccerRules


class RCSSRules(SoccerRules):
    """
    Rule book for the RoboCup Soccer Simulation league.
    """

    def __init__(self,
                 duration: float | None = None,
                 overtime: float | None = None,
                 kick_off_time: float | None = None,
                 throw_in_time: float | None = None) -> None:
        """
        Construct a new RoboCup Soccer Simulation rule book.
        """

        super().__init__(
            match_duration = 2 * 300 if duration is None else duration,
            match_overtime = 2 * 180 if overtime is None else overtime,
            kick_off_time = 15 if kick_off_time is None else kick_off_time,
            throw_in_time = 15 if throw_in_time is None else throw_in_time
        )
