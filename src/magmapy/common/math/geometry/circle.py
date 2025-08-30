from __future__ import annotations

from typing import Final

from magmapy.common.math.geometry.vector import Vector2D


class Circle2D:
    """
    A circle in 2D.
    """

    def __init__(self, origin: Vector2D, radius: float) -> None:
        """
        Construct a new circle.
        """

        self.origin: Final[Vector2D] = origin
        self.radius: Final[float] = radius

    @staticmethod
    def from_coordinates(x: float = 0, y: float = 0, radius: float = 0) -> Circle2D:
        """
        Construct a new circle form the given coordinates.
        """

        return Circle2D(Vector2D(x, y), radius)
