from __future__ import annotations


class Vector2D:
    """
    2-dimensional point or vector.
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Construct a new 2D vector.
        """

        self._x: float = x
        self._y: float = y

    def x(self) -> float:
        """
        Retrieve the x-coordinate of the vector.
        """

        return self._x

    def y(self) -> float:
        """
        Retrieve the y-coordinate of the vector.
        """

        return self._y

    def __str__(self) -> str:
        return f'({self._x}, {self._y})'

    def __repr__(self) -> str:
        return f'Vector2D({self._x}, {self._y})'


class Vector3D:
    """
    3-dimensional point or vector.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        """
        Construct a new 3D vector.
        """

        self._x: float = x
        self._y: float = y
        self._z: float = z

    def x(self) -> float:
        """
        Retrieve the x-coordinate of the vector.
        """

        return self._x

    def y(self) -> float:
        """
        Retrieve the y-coordinate of the vector.
        """

        return self._y

    def z(self) -> float:
        """
        Retrieve the z-coordinate of the vector.
        """

        return self._z

    def as_2d(self) -> Vector2D:
        """
        Retrieve the 2D portion of the vector.
        """

        return Vector2D(self._x, self._y)

    def __str__(self) -> str:
        return f'({self._x}, {self._y}, {self._z})'

    def __repr__(self) -> str:
        return f'Vector2D({self._x}, {self._y}, {self._z})'
