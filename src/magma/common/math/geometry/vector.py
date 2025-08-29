from __future__ import annotations

from math import cos, isfinite, isinf, isnan, sin, sqrt
from typing import Final


class Vector2D:
    """
    2-dimensional point or vector.
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Construct a new 2D vector.
        """

        self.x: Final[float] = x
        self.y: Final[float] = y

    def __add__(self, other: Vector2D) -> Vector2D:
        """
        Element-wise addition.
        """

        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        """
        Element-wise subtraction.
        """

        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2D:
        """
        Element-wise multiplication with scalar.
        """

        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector2D:
        """
        Element-wise multiplication with scalar (from right).
        """

        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector2D:
        """
        Element-wise division with scalar.
        """

        return Vector2D(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: float) -> Vector2D:
        """
        Element-wise integer division (floor division).
        """

        return Vector2D(self.x // scalar, self.y // scalar)

    def __neg__(self) -> Vector2D:
        """
        Element-wise negation.
        """

        return Vector2D(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y

        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def dot(self, other: Vector2D) -> float:
        """
        Calculate the dot product of this vector and the other vector.
        """

        return self.x * other.x + self.y * other.y

    def isfinite(self) -> bool:
        """
        Check if all elements of this vector are finite.
        """

        return isfinite(self.x) and isfinite(self.y)

    def isinf(self) -> bool:
        """
        Check if one of the elements are positive or negative infinite.
        """

        return isinf(self.x) or isinf(self.y)

    def isnan(self) -> bool:
        """
        Check if one of the elements are NaN.
        """

        return isnan(self.x) or isnan(self.y)

    def vector_to(self, other: Vector2D) -> Vector2D:
        """
        Return the vector from this vector to the other vector.
        """

        return other - self

    def direction_to(self, other: Vector2D) -> Vector2D:
        """
        Return the unit vector pointing from this vector the the given vector.
        """

        x = other.x - self.x
        y = other.y - self.y
        length = sqrt(x**2 + y**2)

        return Vector2D(x / length, y / length)

    def norm(self) -> float:
        """
        Return the vector norm.
        """

        return sqrt(self.x**2 + self.y**2)

    def norm_sq(self) -> float:
        """
        Return the squared vector norm.
        """

        return self.x**2 + self.y**2

    def distance(self, other: Vector2D) -> float:
        """
        Return the euclidean distance to the other vector.
        """

        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def distance_sq(self, other: Vector2D) -> float:
        """
        Return the squared euclidean distance to the other vector.
        """

        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __str__(self) -> str:
        return f'({self.x:.4f}, {self.y:.4f})'

    def __repr__(self) -> str:
        return f'Vector2D({self.x:.4f}, {self.y:.4f})'


V2D_ZERO: Final[Vector2D] = Vector2D(0, 0)
"""
The zero vector: (0, 0).
"""


V2D_ONES: Final[Vector2D] = Vector2D(1, 1)
"""
The ones vector: (1, 1).
"""


V2D_UNIT_X: Final[Vector2D] = Vector2D(1, 0)
"""
The unit vector in x direction: (1, 0).
"""


V2D_UNIT_Y: Final[Vector2D] = Vector2D(0, 1)
"""
The unit vector in y direction: (0, 1).
"""


V2D_NEG_ONES: Final[Vector2D] = Vector2D(-1, -1)
"""
The negative ones vector: (-1, -1).
"""


V2D_UNIT_NEG_X: Final[Vector2D] = Vector2D(-1, 0)
"""
The unit vector in negative x direction: (-1, 0).
"""


V2D_UNIT_NEG_Y: Final[Vector2D] = Vector2D(0, -1)
"""
The unit vector in negative y direction: (0, -1).
"""


class Vector3D:
    """
    3-dimensional point or vector.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        """
        Construct a new 3D vector.
        """

        self.x: Final[float] = x
        self.y: Final[float] = y
        self.z: Final[float] = z

    @staticmethod
    def from_pol(alpha: float, delta: float, distance: float) -> Vector3D:
        """Construct a new 3D vector from polar / spherical coordinates."""

        cos_delta = cos(delta)
        x = distance * cos(alpha) * cos_delta
        y = distance * sin(alpha) * cos_delta
        z = distance * sin(delta)

        return Vector3D(x, y, z)

    def as_2d(self) -> Vector2D:
        """
        Retrieve the 2D portion of the vector.
        """

        return Vector2D(self.x, self.y)

    def __add__(self, other: Vector3D) -> Vector3D:
        """
        Element-wise addition.
        """

        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        """
        Element-wise subtraction.
        """

        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3D:
        """
        Element-wise multiplication with scalar.
        """

        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vector3D:
        """
        Element-wise multiplication with scalar (from right).
        """

        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector3D:
        """
        Element-wise division with scalar.
        """

        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __floordiv__(self, scalar: float) -> Vector3D:
        """
        Element-wise integer division (floor division).
        """

        return Vector3D(self.x // scalar, self.y // scalar, self.z // scalar)

    def __neg__(self) -> Vector3D:
        """
        Element-wise negation.
        """

        return Vector3D(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector3D):
            return self.x == other.x and self.y == other.y and self.z == other.z

        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def dot(self, other: Vector3D) -> float:
        """
        Calculate the dot product of this vector and the other vector.
        """

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        """
        Calculate the cross product of this vector and the other vector.
        """

        # fmt: off
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
        # fmt: on

    def isfinite(self) -> bool:
        """
        Check if all elements of this vector are finite.
        """

        return isfinite(self.x) and isfinite(self.y) and isfinite(self.z)

    def isinf(self) -> bool:
        """
        Check if one of the elements are positive or negative infinite.
        """

        return isinf(self.x) or isinf(self.y) or isinf(self.z)

    def isnan(self) -> bool:
        """
        Check if one of the elements are NaN.
        """

        return isnan(self.x) or isnan(self.y) or isnan(self.z)

    def vector_to(self, other: Vector3D) -> Vector3D:
        """
        Return the vector from this vector to the other vector.
        """

        return other - self

    def norm(self) -> float:
        """
        Return the vector norm.
        """

        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm_sq(self) -> float:
        """
        Return the squared vector norm.
        """

        return self.x**2 + self.y**2 + self.z**2

    def distance(self, other: Vector3D) -> float:
        """
        Return the euclidean distance to the other vector.
        """

        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def distance_sq(self, other: Vector3D) -> float:
        """
        Return the squared euclidean distance to the other vector.
        """

        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self) -> str:
        return f'Vector3D({self.x}, {self.y}, {self.z})'


V3D_ZERO: Final[Vector3D] = Vector3D()
"""
The zero vector: (0, 0, 0).
"""


V3D_ONES: Final[Vector3D] = Vector3D(1, 1, 1)
"""
The ones vector: (1, 1, 1).
"""


V3D_UNIT_X: Final[Vector3D] = Vector3D(1, 0, 0)
"""
The unit vector in x direction: (1, 0, 0).
"""


V3D_UNIT_Y: Final[Vector3D] = Vector3D(0, 1, 0)
"""
The unit vector in y direction: (0, 1, 0).
"""


V3D_UNIT_Z: Final[Vector3D] = Vector3D(0, 0, 1)
"""
The unit vector in z direction: (0, 0, 1).
"""


V3D_NEG_ONES: Final[Vector3D] = Vector3D(-1, -1, -1)
"""
The ones vector: (-1, -1, -1).
"""


V3D_UNIT_NEG_X: Final[Vector3D] = Vector3D(-1, 0, 0)
"""
The unit vector in negative x direction: (-1, 0, 0).
"""


V3D_UNIT_NEG_Y: Final[Vector3D] = Vector3D(0, -1, 0)
"""
The unit vector in negative y direction: (0, -1, 0).
"""


V3D_UNIT_NEG_Z: Final[Vector3D] = Vector3D(0, 0, -1)
"""
The unit vector in negative z direction: (0, 0, -1).
"""
