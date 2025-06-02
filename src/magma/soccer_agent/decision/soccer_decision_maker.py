from __future__ import annotations

from typing import TYPE_CHECKING

from magma.agent.decision.behavior import BehaviorID
from magma.agent.decision.decision_maker import DecisionMakerBase
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel

if TYPE_CHECKING:
    from collections.abc import Callable

    from magma.agent.decision.behavior import PBehavior


class SoccerDecisionMaker(DecisionMakerBase[PSoccerAgentModel]):
    """
    Decision maker for playing soccer.
    """

    def __init__(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> None:
        """
        Construct a new soccer decision maker.
        """

        super().__init__(model, behaviors)

        self._behavior_suppliers: list[Callable[[], str | None]] = [
            self._get_ready,
            self._react_to_game_end,
            self._wait_for_game_start,
            self._move,
        ]

    def _decide_next_behavior(self) -> str:
        for supplier in self._behavior_suppliers:
            behavior = supplier()
            if behavior is not None:
                return behavior

        return BehaviorID.NONE.value

    def _get_ready(self) -> str | None:
        """
        Decide if we should get into ready posture.
        """

        return None

    def _react_to_game_end(self) -> str | None:
        """
        Decide for an appropriate behavior to celebrate our victory!

        Note: The default implementation also covers the very unlikely edge case that we didn't win... ;)
        """

        return None

    def _wait_for_game_start(self) -> str | None:
        """
        Decide if we should wait for game start or not.
        Default implementation waits.
        """

        return None

    def _move(self) -> str | None:
        """
        Decide if we should move somewhere or something.
        """

        return None
