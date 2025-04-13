from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol


class BehaviorID(Enum):
    """
    Enum specifying behavior names.
    """

    NONE = "none"
    """
    The none behavior used to do nothing.
    """


class PBehavior(Protocol):
    """
    Base protocol for behaviors.
    """

    def get_name(self) -> str:
        """
        Retrieve the unique name of the behavior.
        """

    def perform(self) -> None:
        """
        Perform the next step of this behavior.
        """

    def is_finished(self) -> bool:
        """
        Check if the behavior is finished.
        """

    def switch_to(self, behavior: PBehavior) -> PBehavior:
        """
        Try switching to the given behavior.
        """


class Behavior(ABC):
    """
    The behavior class for representing agent action threads.
    """

    def __init__(self, name: str) -> None:
        """
        Construct a new behavior.
        """

        self._name = name


    def get_name(self) -> str:
        """
        Retrieve the unique name of the behavior.
        """

        return self._name

    @abstractmethod
    def perform(self) -> None:
        """
        Perform the next step of this behavior.
        """

    @abstractmethod
    def is_finished(self) -> bool:
        """
        Check if the behavior is finished.
        """

    def switch_to(self, behavior: PBehavior) -> PBehavior:
        """
        Try switching to the given behavior.
        """

        return behavior if self.is_finished() else self


class NoneBehavior(Behavior):
    """
    A behavior that does nothing.
    """

    def __init__(self) -> None:
        """
        Construct a new none-behavior.
        """
        super().__init__(BehaviorID.NONE.value)

    def perform(self) -> None:
        # does intentionally nothing
        pass

    def is_finished(self) -> bool:
        return True
