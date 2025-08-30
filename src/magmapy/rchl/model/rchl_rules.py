from __future__ import annotations

from magmapy.soccer_agent.model.soccer_rules import SoccerRules


class RCHLRules(SoccerRules):
    """Rule book for the RoboCup Humanoid League league."""

    def __init__(
        self,
        duration: float | None = None,
        overtime: float | None = None,
        kick_off_time: float | None = None,
        throw_in_time: float | None = None,
    ) -> None:
        """Construct a new RoboCup Humanoid League rule book."""

        super().__init__(
            match_duration=2 * 600 if duration is None else duration,
            match_overtime=2 * 300 if overtime is None else overtime,
            kick_off_time=10 if kick_off_time is None else kick_off_time,
            throw_in_time=10 if throw_in_time is None else throw_in_time,
        )
