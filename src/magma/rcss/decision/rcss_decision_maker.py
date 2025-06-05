from __future__ import annotations

from typing import TYPE_CHECKING

from magma.soccer_agent.decision.soccer_decision_maker import SoccerDecisionMaker

if TYPE_CHECKING:
    from magma.agent.decision.behavior import PBehavior
    from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


class RCSSDecisionMaker(SoccerDecisionMaker):
    """Decision maker for playing soccer."""

    def __init__(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> None:
        """Construct a new soccer decision maker.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.

        behaviors : dict[str, PBehavior]
            The map of known behaviors.
        """

        super().__init__(model, behaviors)

    def _get_ready(self) -> str | None:
        return None

    def _react_to_game_end(self) -> str | None:
        return None

    def _wait_for_game_start(self) -> str | None:
        return None

    def _move(self) -> str | None:
        return None
