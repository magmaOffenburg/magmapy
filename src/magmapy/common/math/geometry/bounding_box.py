from __future__ import annotations

from typing import Final

from magmapy.common.math.geometry.vector import Vector2D, Vector3D


class AABB2D:
    """
    2-dimensional axis-aligned bounding-box.
    """

    def __init__(self, min_x: float = -1, max_x: float = 1, min_y: float = -1, max_y: float = 1) -> None:
        """
        Construct a new 2D axis-aligned bounding-box.
        """

        if min_x > max_x:
            min_x, max_x = max_x, min_x

        if min_y > max_y:
            min_y, max_y = max_y, min_y

        self.min_x: Final[float] = min_x
        self.max_x: Final[float] = max_x
        self.min_y: Final[float] = min_y
        self.max_y: Final[float] = max_y

    def get_width(self) -> float:
        """
        Retrieve the width (in x direction) of the bounding box.
        """

        return self.max_x - self.min_x

    def get_height(self) -> float:
        """
        Retrieve the height (in y direction) of the bounding box.
        """

        return self.max_y - self.min_y

    def get_top_left(self) -> Vector2D:
        """
        Retrieve the top left position of the bounding box.
        """

        return Vector2D(self.min_x, self.max_y)

    def get_top_left_3d(self) -> Vector3D:
        """
        Retrieve the top left position of the bounding box in 3D.
        """

        return Vector3D(self.min_x, self.max_y, 0)

    def get_top_right(self) -> Vector2D:
        """
        Retrieve the top right position of the bounding box.
        """

        return Vector2D(self.max_x, self.max_y)

    def get_top_right_3d(self) -> Vector3D:
        """
        Retrieve the top right position of the bounding box in 3D.
        """

        return Vector3D(self.max_x, self.max_y, 0)

    def get_bottom_left(self) -> Vector2D:
        """
        Retrieve the bottom left position of the bounding box.
        """

        return Vector2D(self.min_x, self.min_y)

    def get_bottom_left_3d(self) -> Vector3D:
        """
        Retrieve the bottom left position of the bounding box in 3D.
        """

        return Vector3D(self.min_x, self.min_y, 0)

    def get_bottom_right(self) -> Vector2D:
        """
        Retrieve the bottom right position of the bounding box.
        """

        return Vector2D(self.max_x, self.min_y)

    def get_bottom_right_3d(self) -> Vector3D:
        """
        Retrieve the bottom right position of the bounding box in 3D.
        """

        return Vector3D(self.max_x, self.min_y, 0)

    def get_center(self) -> Vector2D:
        """
        Retrieve the center position of the bounding box.
        """

        return Vector2D(self.min_x + self.get_width() / 2, self.min_y + self.get_height() / 2)

    def get_center_3d(self) -> Vector3D:
        """
        Retrieve the center position of the bounding box in 3D.
        """

        return Vector3D(self.min_x + self.get_width() / 2, self.min_y + self.get_height() / 2, 0)

    def contains_x(self, x: float) -> bool:
        """
        Check if the given x-coordinate is within the bounding box.
        """

        return self.min_x <= x and x <= self.max_x

    def contains_y(self, y: float) -> bool:
        """
        Check if the given y-coordinate is within the bounding box.
        """

        return self.min_y <= y and y <= self.max_y

    def contains_xy(self, x: float, y: float) -> bool:
        """
        Check if the given x- and y-coordinate is within the bounding box.
        """

        return self.min_x <= x and x <= self.max_x and self.min_y <= y and y <= self.max_y

    def contains(self, point: Vector2D | Vector3D) -> bool:
        """
        Check if the given point is within the bounding box.
        """

        return self.contains_xy(point.x, point.y)

    def apply_border(self, *, border_x: float | None = None, border_y: float | None = None, border: float | None = None) -> AABB2D:
        """
        Apply a border around the bounding-box.
        """

        if border is None:
            border = 0

        if border_x is None:
            border_x = border

        if border_y is None:
            border_y = border

        return AABB2D(self.min_x - border_x, self.max_x + border_x, self.min_y - border_y, self.max_y + border_y)

    def clip(self, pos: Vector2D) -> Vector2D:
        """Clip the given point within the area."""

        x = pos.x
        y = pos.y

        if x < self.min_x:
            x = self.min_x
        elif x > self.max_x:
            x = self.max_x

        if y < self.min_y:
            y = self.min_y
        elif y > self.max_y:
            y = self.max_y

        return Vector2D(x, y)
