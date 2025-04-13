from __future__ import annotations

from typing import TYPE_CHECKING

from magma.rcss.decision.rcss_base_behaviors import RCSSBehaviorID
from magma.soccer_agent.decision.soccer_decision_maker import SoccerDecisionMaker

if TYPE_CHECKING:
    from magma.agent.decision.behavior import PBehavior
    from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


class RCSSDecisionMaker(SoccerDecisionMaker):
    """
    Decision maker for playing soccer.
    """

    def __init__(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> None:
        """
        Construct a new soccer decision maker.
        """

        super().__init__(model, behaviors)

        self._create_behavior: PBehavior = self._behaviors[RCSSBehaviorID.CREATE.value]
        self._init_behavior: PBehavior = self._behaviors[RCSSBehaviorID.INIT.value]

    def _setup(self) -> str | None:
        if not self._create_behavior.is_finished():
            return self._create_behavior.get_name()

        if not self._init_behavior.is_finished():
            return self._init_behavior.get_name()

        return None

    def _get_ready(self) -> str | None:
        return None

    def _react_to_game_end(self) -> str | None:
        return None

    def _wait_for_game_start(self) -> str | None:
        return None

    def _move(self) -> str | None:
        return None
