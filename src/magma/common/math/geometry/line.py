from __future__ import annotations

from typing import Final

from magma.common.math.geometry.vector import V2D_ZERO, Vector2D


class LineSegment2D:
    """
    2-dimensional line segment.
    """

    def __init__(self, start: Vector2D | None = None, end: Vector2D | None = None) -> None:
        """
        Construct a new 2D pose.
        """

        self.start: Final[Vector2D] = V2D_ZERO if start is None else start
        self.end: Final[Vector2D] = V2D_ZERO if end is None else end

    @staticmethod
    def from_coordinates(x_start: float = 0, y_start: float = 0, x_end: float = 0, y_end: float = 0) -> LineSegment2D:
        """
        Construct a new line segment form the given coordinates.
        """

        return LineSegment2D(Vector2D(x_start, y_start), Vector2D(x_end, y_end))
