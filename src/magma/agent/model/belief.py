from abc import ABC, abstractmethod
from typing import Protocol


class PBelief(Protocol):
    """Protocol for beliefs representing a truth value."""

    def is_true(self) -> bool:
        """Check if the belief is considered true."""

    def is_false(self) -> bool:
        """Check if the belief is considered false."""

    def get_since(self) -> float:
        """Retrieve the time since this belief is in its current state."""


class Belief(ABC):
    """Base implementation for beliefs representing a truth value."""

    def __init__(self) -> None:
        """Construct a new belief."""

        self._valid: bool = False
        """Flag if this belief is currently valid."""

        self._since: float = 0.0
        """Time of the last state change."""

    def is_true(self) -> bool:
        """Check if the belief is considered true."""

        return self._valid

    def is_false(self) -> bool:
        """Check if the belief is considered false."""

        return not self._valid

    def get_since(self) -> float:
        """Retrieve the time since this belief is in its current state."""

        return self._since

    @abstractmethod
    def update(self) -> bool:
        """Update this belief from model information."""

    def __bool__(self) -> bool:
        return self._valid
