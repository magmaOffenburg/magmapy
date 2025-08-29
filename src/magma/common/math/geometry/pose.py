from __future__ import annotations

from typing import Final

from magma.common.math.geometry.angle import ANGLE_ZERO, Angle2D, rotate_2d
from magma.common.math.geometry.rotation import R3D_IDENTITY, Rotation3D
from magma.common.math.geometry.vector import V2D_ZERO, V3D_ZERO, Vector2D, Vector3D


class Pose2D:
    """
    2-dimensional pose.
    """

    def __init__(self, pos: Vector2D | None = None, theta: Angle2D | None = None) -> None:
        """
        Construct a new 2D pose.
        """

        self.pos: Final[Vector2D] = V2D_ZERO if pos is None else pos
        self.theta: Final[Angle2D] = ANGLE_ZERO if theta is None else theta

    @staticmethod
    def from_coordinates(x: float = 0, y: float = 0, theta: float = 0) -> Pose2D:
        """
        Construct a new 2D pose form the given coordinates.
        """

        return Pose2D(Vector2D(x, y), Angle2D(theta))

    def x(self) -> float:
        """
        Retrieve the x-coordinate of the pose.
        """

        return self.pos.x

    def y(self) -> float:
        """
        Retrieve the y-coordinate of the pose.
        """

        return self.pos.y

    def tf_vec(self, v: Vector2D) -> Vector2D:
        """
        Transform the given vector by this transformation.
        """

        tx, ty = rotate_2d(v.x, v.y, self.theta.rad())

        return Vector2D(self.pos.x + tx, self.pos.y + ty)

    def inv_tf_vec(self, v: Vector2D) -> Vector2D:
        """
        Inverse transform the given vector by this transformation.
        """

        return Vector2D(*rotate_2d(v.x - self.pos.x, v.y - self.pos.y, -self.theta.rad()))

    def tf_pose(self, p: Pose2D) -> Pose2D:
        """
        Transform the given pose by this transformation.
        """

        return Pose2D(self.tf_vec(p.pos), self.theta + p.theta)

    def inv_tf_pose(self, p: Pose2D) -> Pose2D:
        """
        Inverse transform the given pose by this transformation.
        """

        return Pose2D(self.inv_tf_vec(p.pos), p.theta - self.theta)

    def tf_rot(self, r: Angle2D) -> Angle2D:
        """
        Transform the given rotation by this transformation.
        """

        return self.theta.tf_rot(r)

    def inv_tf_rot(self, r: Angle2D) -> Angle2D:
        """
        Inverse transform the given rotation by this transformation.
        """

        return self.theta.inv_tf_rot(r)

    def __str__(self) -> str:
        return f'{self.pos}, {self.theta}'

    def __repr__(self) -> str:
        return f'Pose2D({self.pos}, {self.theta})'


P2D_ZERO: Final[Pose2D] = Pose2D()
"""
The zero 2D pose.
"""


class Pose3D:
    """
    3-dimensional pose.
    """

    def __init__(self, pos: Vector3D | None = None, rot: Rotation3D | None = None) -> None:
        """
        Construct a new 3D pose.
        """

        self.pos: Final[Vector3D] = V3D_ZERO if pos is None else pos
        self.rot: Final[Rotation3D] = R3D_IDENTITY if rot is None else rot

    @staticmethod
    def from_coordinates(x: float = 0, y: float = 0, z: float = 0, rot: Rotation3D | None = None) -> Pose3D:
        """
        Construct a new 3D pose form the given coordinates.
        """

        return Pose3D(Vector3D(x, y, z), rot)

    def x(self) -> float:
        """
        Retrieve the x-coordinate of the pose.
        """

        return self.pos.x

    def y(self) -> float:
        """
        Retrieve the y-coordinate of the pose.
        """

        return self.pos.y

    def z(self) -> float:
        """
        Retrieve the z-coordinate of the pose.
        """

        return self.pos.z

    def tf_vec(self, v: Vector3D) -> Vector3D:
        """
        Transform the given vector by this transformation.
        """

        return self.pos + self.rot.tf_vec(v)

    def inv_tf_vec(self, v: Vector3D) -> Vector3D:
        """
        Inverse transform the given vector by this transformation.
        """

        return self.rot.inv_tf_vec(v - self.pos)

    def tf_pose(self, p: Pose3D) -> Pose3D:
        """
        Transform the given pose by this transformation.
        """

        return Pose3D(self.tf_vec(p.pos), self.rot.tf_rot(p.rot))

    def inv_tf_pose(self, p: Pose3D) -> Pose3D:
        """
        Inverse transform the given pose by this transformation.
        """

        return Pose3D(self.inv_tf_vec(p.pos), self.rot.inv_tf_rot(p.rot))

    def tf_rot(self, r: Rotation3D) -> Rotation3D:
        """
        Transform the given rotation by this transformation.
        """

        return self.rot.tf_rot(r)

    def inv_tf_rot(self, r: Rotation3D) -> Rotation3D:
        """
        Inverse transform the given rotation by this transformation.
        """

        return self.rot.inv_tf_rot(r)

    def __str__(self) -> str:
        return f'{self.pos}\n{self.rot}'

    def __repr__(self) -> str:
        return f'Pose3D({self.pos}, {self.rot})'


P3D_ZERO: Final[Pose3D] = Pose3D()
"""
The zero 3D pose.
"""
