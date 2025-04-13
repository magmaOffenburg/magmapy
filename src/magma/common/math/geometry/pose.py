from __future__ import annotations

from magma.common.math.geometry.rotation import Rotation2D, Rotation3D
from magma.common.math.geometry.vector import Vector2D, Vector3D


class Pose2D:
    """
    2-dimensional pose.
    """

    def __init__(self, pos: Vector2D | None = None, theta: Rotation2D | None = None) -> None:
        """
        Construct a new 2D pose.
        """

        self._pos: Vector2D = Vector2D() if pos is None else pos
        self._theta: Rotation2D = Rotation2D() if theta is None else theta

    @staticmethod
    def from_coordinates(x: float = 0, y: float = 0, theta: float = 0) -> Pose2D:
        """
        Construct a new 2D pose form the given coordinates.
        """

        return Pose2D(Vector2D(x, y), Rotation2D(theta))

    def position(self) -> Vector2D:
        """
        Retrieve the position part of the pose.
        """

        return self._pos

    def x(self) -> float:
        """
        Retrieve the x-coordinate of the pose.
        """

        return self._pos.x()

    def y(self) -> float:
        """
        Retrieve the y-coordinate of the pose.
        """

        return self._pos.y()

    def theta(self) -> Rotation2D:
        """
        Retrieve the horizontal orientation.
        """

        return self._theta


class Pose3D:
    """
    3-dimensional pose.
    """

    def __init__(self, pos: Vector3D | None = None, rot: Rotation3D | None = None) -> None:
        """
        Construct a new 3D pose.
        """

        self._pos: Vector3D = Vector3D() if pos is None else pos
        self._rot: Rotation3D = Rotation3D() if rot is None else rot

    @staticmethod
    def from_coordinates(x: float = 0, y: float = 0, z: float = 0, rot: Rotation3D | None = None) -> Pose3D:
        """
        Construct a new 3D pose form the given coordinates.
        """

        return Pose3D(Vector3D(x, y, z), rot)

    def position(self) -> Vector3D:
        """
        Retrieve the position part of the pose.
        """

        return self._pos

    def orientation(self) -> Rotation3D:
        """
        Retrieve the orientation part of the pose.
        """

        return self._rot

    def x(self) -> float:
        """
        Retrieve the x-coordinate of the pose.
        """

        return self._pos.x()

    def y(self) -> float:
        """
        Retrieve the y-coordinate of the pose.
        """

        return self._pos.y()

    def z(self) -> float:
        """
        Retrieve the z-coordinate of the pose.
        """

        return self._pos.z()
