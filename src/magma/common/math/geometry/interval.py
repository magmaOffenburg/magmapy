from typing import Final


class Interval:
    """A 1D interval."""

    def __init__(self, min_val: float, max_val: float) -> None:
        """Construct a new 1D interval."""

        if min_val > max_val:
            max_val, min_val = min_val, max_val

        self.min: Final[float] = min_val
        """The minimum value of the interval."""

        self.max: Final[float] = max_val
        """the maximum value of the interval."""

    def get_range(self) -> float:
        """Retrieve the interval range (distance between min and max)."""

        return self.max - self.min

    def get_center(self) -> float:
        """Retrieve center of the interval."""

        return (self.min + self.max) / 2

    def contains(self, value: float) -> bool:
        """Check if the given value is within the interval."""

        return self.min <= value and value <= self.max

    def clamp(self, value: float) -> float:
        """Clamp the given value within this interval.

        Parameter
        ---------
        value : float
            The value to clamp.
        """

        if value < self.min:
            return self.min

        if value > self.max:
            return self.max

        return value
