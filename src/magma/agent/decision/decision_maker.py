from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Protocol, TypeVar

from magma.agent.decision.behavior import BehaviorID
from magma.agent.model.agent_model import PAgentModel

if TYPE_CHECKING:
    from collections.abc import Mapping

    from magma.agent.decision.behavior import PBehavior


class PDecisionMaker(Protocol):
    """
    Base protocol for decision makers.
    """

    def get_behaviors(self) -> Mapping[str, PBehavior]:
        """
        Retrieve the map of known behaviors.
        """

    def get_no_of_decisions(self) -> int:
        """
        Retrieve the number of taken decisions.
        """

    def get_current_behavior(self) -> PBehavior:
        """
        Retrieve the currently active behavior.
        """

    def get_desired_behavior(self) -> PBehavior:
        """
        Retrieve the desired behavior.
        """

    def decide(self) -> None:
        """
        Take a decision based on the current state and perform and action.
        """


MT = TypeVar('MT')


class DecisionMakerBase(Generic[MT], ABC):
    """
    Base class for decision makers.
    """

    def __init__(self, model: MT, behaviors: dict[str, PBehavior]) -> None:
        """
        Construct a new decision maker.
        """

        self._decision_counter: int = 0
        self._model: MT = model
        self._behaviors: dict[str, PBehavior] = behaviors
        self._current_behavior: PBehavior = self._behaviors[BehaviorID.NONE.value]
        self._desired_behavior: PBehavior = self._behaviors[BehaviorID.NONE.value]

    def get_behaviors(self) -> Mapping[str, PBehavior]:
        """
        Retrieve the map of known behaviors.
        """

        return self._behaviors

    def get_no_of_decisions(self) -> int:
        """
        Retrieve the number of taken decisions.
        """

        return self._decision_counter

    def get_current_behavior(self) -> PBehavior:
        """
        Retrieve the currently active behavior.
        """

        return self._current_behavior

    def get_desired_behavior(self) -> PBehavior:
        """
        Retrieve the desired behavior.
        """

        return self._desired_behavior

    def decide(self) -> None:
        """
        Take a decision based on the current state and perform an action.
        """

        # decide for next behavior
        desired_behavior_id = self._decide_next_behavior()
        if desired_behavior_id in self._behaviors:
            self._desired_behavior = self._behaviors[desired_behavior_id]
        else:
            print(f'WARNING: Desired behavior with name "{desired_behavior_id}" not found in behavior map!')  # noqa: T201

        # try switching to the requested behavior
        if self._desired_behavior != self._current_behavior:
            self._current_behavior = self._current_behavior.switch_to(self._desired_behavior)

        # perform current behavior
        # print(f'Performing {self._decision_counter}: {self._current_behavior.get_name()}')
        self._current_behavior.perform()

        # increment decision counter
        self._decision_counter += 1

    @abstractmethod
    def _decide_next_behavior(self) -> str:
        """
        Take a decision based on the current state.
        """


class NoneDecisionMaker(DecisionMakerBase[PAgentModel]):
    """
    A decision maker that does nothing.
    """

    def __init__(self, model: PAgentModel, behaviors: dict[str, PBehavior] | None = None) -> None:
        """
        Construct a new none decision maker.
        """

        super().__init__(model, {} if behaviors is None else behaviors)

    def _decide_next_behavior(self) -> str:
        # does intentionally nothing
        return BehaviorID.NONE.value
