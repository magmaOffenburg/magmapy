from abc import ABC, abstractmethod
from typing import Final, Protocol


class PBelief(Protocol):
    """Protocol for beliefs representing a truth value."""

    def is_true(self) -> bool:
        """Check if the belief is considered true."""

    def is_false(self) -> bool:
        """Check if the belief is considered false."""

    def get_since(self) -> float:
        """Retrieve the time since this belief is in its current state."""

    def __bool__(self) -> bool:
        """Check if the belief is considered true."""


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

    def _set_valid(self, valid: bool, time: float) -> None:  # noqa: FBT001
        """Set the state of this belief.

        Parameter
        ---------
        valid : bool
            The current / new state of the belief.

        time: float
            The current time.
        """

        if self._valid != valid:
            self._since = time

        self._valid = valid

    @abstractmethod
    def update(self) -> bool:
        """Update this belief from model information."""

    def __bool__(self) -> bool:
        return self._valid


class HysteresisBelief(Belief, ABC):
    """Base implementation for hysteresis based beliefs."""

    def __init__(
        self,
        lower_bound: float,
        upper_bound: float,
        *,
        low_is_true: bool = True,
    ) -> None:
        """Construct a hysteresis belief.

        Parameter
        ---------
        lower_bound : float
            The lower bound value of the hysteresis function.

        upper_bound : float
            The upper bound value of the hysteresis function.

        low_is_true : bool, default=True
            Flag indicating the direction (below lower bound / above upper bound) of truth.
        """

        super().__init__()

        self.lower_bound: Final[float] = lower_bound
        """The lower bound value of the hysteresis function."""

        self.upper_bound: Final[float] = upper_bound
        """The upper bound value of the hysteresis function."""

        self.low_is_true: Final[bool] = low_is_true
        """Flag indicating the direction (below lower bound / above upper bound) of truth."""

    def _update_validity(self, value: float, time: float) -> None:
        """Update the truth value of this belief by checking the given value against the lower / upper bounds of the specified hysteresis."""

        if self.low_is_true:
            if self._valid:
                if value > self.upper_bound:
                    self._set_valid(False, time)
            elif value < self.lower_bound:
                self._set_valid(True, time)

        elif self._valid:
            if value < self.lower_bound:
                self._set_valid(False, time)
        elif value > self.upper_bound:
            self._set_valid(True, time)
