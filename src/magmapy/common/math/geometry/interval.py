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

    def clip(self, value: float) -> float:
        """Clip the given value within this interval.

        Parameter
        ---------
        value : float
            The value to clip.
        """

        if value < self.min:
            return self.min

        if value > self.max:
            return self.max

        return value


def clip(value: float, min_val: float, max_val: float) -> float:
    """Clip the value within the interval given by min and max.

    Parameter
    ---------
    value : float
        The value to clip.

    min_val : float
        The minimum value (lower bound).

    max_val : float
        The maximum value (upper bound).
    """

    if value < min_val:
        return min_val

    if value > max_val:
        return max_val

    return value


def clip_abs(value: float, threshold: float) -> float:
    """Clip the value within the absolute interval given by the threshold value.

    Parameter
    ---------
    value : float
        The value to clip.

    threshold : float
        The minimum / maximum value (absolute bound).
    """

    if value < -threshold:
        return -threshold

    if value > threshold:
        return threshold

    return value
