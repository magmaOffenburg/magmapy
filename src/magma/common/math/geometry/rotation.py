from __future__ import annotations

import numpy as np
import numpy.typing as npt


class Rotation2D:
    """
    2-dimensional rotation.
    """

    def __init__(self, rad: float = 0) -> None:
        """
        Construct a new 2D rotation.
        """

        self._angle: float = rad
        self._normalize()

    def _normalize(self) -> None:
        """
        Normalize the rotation angle between +/- PI.
        """

        if self._angle >= 0:
            self._angle = self._angle + np.pi
            self._angle = self._angle % (2 * np.pi)
            self._angle = self._angle - np.pi
        else:
            self._angle = -self._angle + np.pi
            self._angle = self._angle % (2 * np.pi)
            self._angle = -(self._angle - np.pi)
            if self._angle >= np.pi:
                self._angle = -self._angle

    def radians(self) -> float:
        """
        Retrieve the rotation angle in radians.
        """

        return self._angle

    def degrees(self) -> float:
        """
        Retrieve the rotation angle in degrees.
        """

        return self._angle * 180.0 / np.pi

    def add(self, value: float | Rotation2D) -> Rotation2D:
        """
        Add another angle to this angle.
        """

        return Rotation2D(self._angle + value.radians() if isinstance(value, Rotation2D) else value)

    def subtract(self, value: float | Rotation2D) -> Rotation2D:
        """
        Subtract another angle from this angle.
        """

        return Rotation2D(self._angle - value.radians() if isinstance(value, Rotation2D) else value)

    def is_left_of(self, other: Rotation2D) -> bool:
        """
        An angle is "left" of another if it is bigger, but by less than 180 degrees.
        """

        if self._angle > np.pi / 2 and other.radians() < -np.pi / 2:
            # value on -180 degree border
            return False

        if self._angle < -np.pi / 2 and other.radians() > np.pi / 2:
            # value on +180 degree border
            return True

        delta = other.subtract(self._angle).radians()
        return delta < 0 and delta > -np.pi

    def is_right_of(self, other: Rotation2D) -> bool:
        """
        An angle is "right" of another if it is not "left" of it.
        """

        return not self.is_left_of(other)

    def is_between(self, start: Rotation2D, end: Rotation2D) -> bool:
        """
        Check if this angle is between the given start and end angles.
        """

        if start.radians() <= end.radians():
            return self._angle >= start.radians() and self._angle < end.radians()

        # arc contains 180 degrees border
        if self._angle < end.radians():
            return True

        return self._angle >= start.radians()


class Rotation3D:
    """
    3-dimensional rotation.
    """

    def __init__(self, m: npt.NDArray[np.float32] | None = None) -> None:
        """
        Construct a new 3D rotation from the given 3x3 matrix.
        """

        self._m: npt.NDArray[np.float32] = np.identity(3) if m is None else m
