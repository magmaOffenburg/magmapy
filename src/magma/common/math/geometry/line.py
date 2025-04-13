from __future__ import annotations

from magma.common.math.geometry.vector import Vector2D


class LineSegment2D:
    """
    2-dimensional line segment.
    """

    def __init__(self, start: Vector2D | None = None, end: Vector2D | None = None) -> None:
        """
        Construct a new 2D pose.
        """

        self._start: Vector2D = Vector2D() if start is None else start
        self._end: Vector2D = Vector2D() if end is None else end

    @staticmethod
    def from_coordinates(x_start: float = 0, y_start: float = 0, x_end: float = 0, y_end: float = 0) -> LineSegment2D:
        """
        Construct a new line segment form the given coordinates.
        """

        return LineSegment2D(Vector2D(x_start, y_start), Vector2D(x_end, y_end))

    def start_pos(self) -> Vector2D:
        """
        Retrieve the start position of the line.
        """

        return self._start

    def end_pos(self) -> Vector2D:
        """
        Retrieve the line extension from the start point.
        """

        return self._end
