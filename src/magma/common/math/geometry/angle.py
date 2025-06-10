from __future__ import annotations

from math import atan2, cos, degrees, pi, radians, sin
from typing import Final

import magma.common.math.geometry.pose as p2d
from magma.common.math.geometry.vector import Vector2D


class Angle2D:
    """
    2-dimensional angle / rotation.
    """

    def __init__(self, angle: float = 0) -> None:
        """
        Construct a new 2D angle / rotation from the given radian angle.
        """

        # normalize the rotation angle between +/- PI.
        if angle >= 0:
            angle += pi
            angle = angle % (2 * pi)
            angle -= pi
        else:
            angle = -angle + pi
            angle = angle % (2 * pi)
            angle = -(angle - pi)
            if angle >= pi:
                angle = -angle

        self.angle: Final[float] = angle

    def rad(self) -> float:
        """
        Retrieve the rotation angle in radians.
        """

        return self.angle

    def deg(self) -> float:
        """
        Retrieve the rotation angle in degrees.
        """

        return degrees(self.angle)

    def __add__(self, value: float | Angle2D) -> Angle2D:
        """
        Add another angle to this angle.
        """

        return Angle2D(self.angle + (value.angle if isinstance(value, Angle2D) else value))

    def __sub__(self, value: float | Angle2D) -> Angle2D:
        """
        Subtract another angle from this angle.
        """

        return Angle2D(self.angle - (value.angle if isinstance(value, Angle2D) else value))

    def __neg__(self) -> Angle2D:
        """
        Return a negated angle / inverse rotation.
        """

        return Angle2D(-self.angle)

    def __abs__(self) -> Angle2D:
        return Angle2D(abs(self.angle))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Angle2D):
            return self.angle == other.angle

        return False

    def __hash__(self) -> int:
        return hash(self.angle)

    def mirror(self) -> Angle2D:
        """
        Return an angle / rotation pointing in the opposite direction.
        """

        return Angle2D(self.angle + pi)

    def is_left_of(self, other: Angle2D) -> bool:
        """
        An angle is "left" of another if it is bigger, but by less than 180 degrees.
        """

        if self.angle > pi / 2 and other.angle < -pi / 2:
            # value on -180 degree border
            return False

        if self.angle < -pi / 2 and other.angle > pi / 2:
            # value on +180 degree border
            return True

        delta = (other - self.angle).rad()
        return delta < 0 and delta > -pi

    def is_right_of(self, other: Angle2D) -> bool:
        """
        An angle is "right" of another if it is not "left" of it.
        """

        return not self.is_left_of(other)

    def is_between(self, start: Angle2D, end: Angle2D) -> bool:
        """
        Check if this angle is between the given start and end angles.
        """

        if start.angle <= end.angle:
            return self.angle >= start.angle and self.angle < end.angle

        # arc contains 180 degrees border
        if self.angle < end.angle:
            return True

        return self.angle >= start.angle

    def tf_vec(self, v: Vector2D) -> Vector2D:
        """
        Transform the given vector by this rotation.
        """

        return Vector2D(*rotate_2d(v.x, v.y, self.angle))

    def inv_tf_vec(self, v: Vector2D) -> Vector2D:
        """
        Inverse transform the given vector by this rotation.
        """

        return Vector2D(*rotate_2d(v.x, v.y, -self.angle))

    def tf_pose(self, p: p2d.Pose2D) -> p2d.Pose2D:
        """
        Transform the given pose by this rotation.
        """

        return p2d.Pose2D(self.tf_vec(p.pos), self + p.theta)

    def inv_tf_pose(self, p: p2d.Pose2D) -> p2d.Pose2D:
        """
        Inverse transform the given pose by this rotation.
        """

        return p2d.Pose2D(self.inv_tf_vec(p.pos), p.theta - self)

    def tf_rot(self, a: Angle2D) -> Angle2D:
        """
        Transform the given angle / rotation by this rotation.
        """

        return self + a

    def inv_tf_rot(self, a: Angle2D) -> Angle2D:
        """
        Inverse transform the given angle / rotation by this rotation.
        """

        return a - self

    def __str__(self) -> str:
        return f'{self.deg():.4f}°'

    def __repr__(self) -> str:
        return f'Angle2D({self.angle:.4f})'


def rotate_2d(x: float, y: float, rad: float) -> tuple[float, float]:
    """
    Rotate the given point by the given angle.
    """

    # [ca -sa] [x]
    # [sa  ca] [y]
    sa = sin(rad)
    ca = cos(rad)
    return ca * x - sa * y, sa * x + ca * y


def angle_rad(rad: float) -> Angle2D:
    """
    Construct a new Angle2D from the given radian angle.
    """

    return Angle2D(rad)


def angle_deg(deg: float) -> Angle2D:
    """
    Construct a new Angle2D from the given degrees angle.
    """

    return Angle2D(radians(deg))


def angle_to(point: Vector2D) -> Angle2D:
    """
    Construct a new Angle2D from the angle to the given point.
    """

    return Angle2D(atan2(point.y, point.x))


def angle_to_xy(x: float, y: float) -> Angle2D:
    """
    Construct a new Angle2D from the angle to the given point.
    """

    return Angle2D(atan2(y, x))


ANGLE_ZERO: Final[Angle2D] = Angle2D(0)
"""
The zero angle / identity rotation.
"""

ANGLE_90: Final[Angle2D] = Angle2D(pi / 2)
"""
The 90 degree angle.
"""

ANGLE_180: Final[Angle2D] = Angle2D(pi)
"""
The 180 degree angle.
"""

ANGLE_N90: Final[Angle2D] = Angle2D(-pi / 2)
"""
The -90 degree angle.
"""

ANGLE_N180: Final[Angle2D] = Angle2D(-pi)
"""
The -180 degree angle.
"""
