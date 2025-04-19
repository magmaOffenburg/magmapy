from __future__ import annotations

from math import cos, sin
from typing import TYPE_CHECKING, Callable, Final

from magma.common.math.geometry.vector import Vector3D

if TYPE_CHECKING:
    from collections.abc import Mapping


class Rotation3D:
    """
    3-dimensional rotation.
    """

    def __init__(self, m11: float, m12: float, m13: float, m21: float, m22: float, m23: float, m31: float, m32: float, m33: float) -> None:
        """
        Construct a new 3D rotation from the given values.
        """

        self.m11: Final[float] = m11
        self.m12: Final[float] = m12
        self.m13: Final[float] = m13

        self.m21: Final[float] = m21
        self.m22: Final[float] = m22
        self.m23: Final[float] = m23

        self.m31: Final[float] = m31
        self.m32: Final[float] = m32
        self.m33: Final[float] = m33

    def tf_vec(self, v: Vector3D) -> Vector3D:
        """
        Transform the given vector by this rotation.
        """

        # fmt: off
        return Vector3D(
            self.m11 * v.x + self.m12 * v.y + self.m13 * v.z,
            self.m21 * v.x + self.m22 * v.y + self.m23 * v.z,
            self.m31 * v.x + self.m32 * v.y + self.m33 * v.z
        )
        # fmt: on

    def inv_tf_vec(self, v: Vector3D) -> Vector3D:
        """
        Inverse transform the given vector by this rotation.
        """

        # fmt: off
        return Vector3D(
            self.m11 * v.x + self.m21 * v.y + self.m31 * v.z,
            self.m12 * v.x + self.m22 * v.y + self.m32 * v.z,
            self.m13 * v.x + self.m23 * v.y + self.m33 * v.z
        )
        # fmt: on

    def tf_rot(self, r: Rotation3D) -> Rotation3D:
        """
        Transform the given vector by this rotation.
        """

        # fmt: off
        return Rotation3D(
            self.m11 * r.m11 + self.m12 * r.m21 + self.m13 * r.m31,
            self.m21 * r.m11 + self.m22 * r.m21 + self.m23 * r.m31,
            self.m31 * r.m11 + self.m32 * r.m21 + self.m33 * r.m31,

            self.m11 * r.m12 + self.m12 * r.m22 + self.m13 * r.m32,
            self.m21 * r.m12 + self.m22 * r.m22 + self.m23 * r.m32,
            self.m31 * r.m12 + self.m32 * r.m22 + self.m33 * r.m32,

            self.m11 * r.m13 + self.m12 * r.m23 + self.m13 * r.m33,
            self.m21 * r.m13 + self.m22 * r.m23 + self.m23 * r.m33,
            self.m31 * r.m13 + self.m32 * r.m23 + self.m33 * r.m33
        )
        # fmt: on

    def inv_tf_rot(self, r: Rotation3D) -> Rotation3D:
        """
        Inverse transform the given vector by this rotation.
        """

        # fmt: off
        return Rotation3D(
            self.m11 * r.m11 + self.m21 * r.m21 + self.m31 * r.m31,
            self.m12 * r.m11 + self.m22 * r.m21 + self.m32 * r.m31,
            self.m13 * r.m11 + self.m23 * r.m21 + self.m33 * r.m31,

            self.m11 * r.m12 + self.m21 * r.m22 + self.m31 * r.m32,
            self.m12 * r.m12 + self.m22 * r.m22 + self.m32 * r.m32,
            self.m13 * r.m12 + self.m23 * r.m22 + self.m33 * r.m32,

            self.m11 * r.m13 + self.m21 * r.m23 + self.m31 * r.m33,
            self.m12 * r.m13 + self.m22 * r.m23 + self.m32 * r.m33,
            self.m13 * r.m13 + self.m23 * r.m23 + self.m33 * r.m33
        )
        # fmt: on


def axis_angle(axis: Vector3D, angle_rad: float) -> Rotation3D:
    """
    Construct a new rotation from the given axis and angle.
    """

    # lookup axis-aligned rotation function
    aar = _AAR_MAP.get(axis)
    if aar:
        return aar(angle_rad)

    sa = sin(angle_rad)
    ca = cos(angle_rad)
    ca1 = 1 - ca

    xx1ca = axis.x * axis.x * ca1
    yy1ca = axis.y * axis.y * ca1
    zz1ca = axis.z * axis.z * ca1
    xy1ca = axis.x * axis.y * ca1
    xz1ca = axis.x * axis.z * ca1
    yz1ca = axis.y * axis.z * ca1

    xsa = axis.x * sa
    ysa = axis.y * sa
    zsa = axis.z * sa

    # fmt: off
    return Rotation3D(
         xx1ca + ca,  xy1ca - zsa,  xz1ca + ysa,
        xy1ca + zsa,   yy1ca + ca,  yz1ca - xsa,
        xz1ca - ysa,  yz1ca + xsa,   zz1ca + ca
    )
    # fmt: on


def rot_x(angle_rad: float) -> Rotation3D:
    """
    Create a 3D rotation around x-axis with the given angle.
    """

    ca = cos(angle_rad)
    sa = sin(angle_rad)

    # fmt: off
    return Rotation3D(
        1,   0,   0,
        0,  ca, -sa,
        0,  sa,  ca
    )
    # fmt: on


def inv_rot_x(angle_rad: float) -> Rotation3D:
    """
    Create a 3D rotation around x-axis with the negated angle.
    """

    return rot_x(-angle_rad)


def rot_y(angle_rad: float) -> Rotation3D:
    """
    Create a rotation around y-axis with the given angle.
    """

    ca = cos(angle_rad)
    sa = sin(angle_rad)

    # fmt: off
    return Rotation3D(
         ca,   0,  sa,
          0,   1,   0,
        -sa,   0,  ca
    )
    # fmt: on


def inv_rot_y(angle_rad: float) -> Rotation3D:
    """
    Create a 3D rotation around y-axis with the negated angle.
    """

    return rot_y(-angle_rad)


def rot_z(angle_rad: float) -> Rotation3D:
    """
    Create a rotation around z-axis with the given angle.
    """

    ca = cos(angle_rad)
    sa = sin(angle_rad)

    # fmt: off
    return Rotation3D(
        ca, -sa,   0,
        sa,  ca,   0,
         0,   0,   1
    )
    # fmt: on


def inv_rot_z(angle_rad: float) -> Rotation3D:
    """
    Create a 3D rotation around z-axis with the negated angle.
    """

    return rot_z(-angle_rad)


_AAR_MAP: Final[Mapping[Vector3D, Callable[[float], Rotation3D]]] = {
    Vector3D(1, 0, 0): rot_x,
    Vector3D(-1, 0, 0): inv_rot_x,
    Vector3D(0, 1, 0): rot_y,
    Vector3D(0, -1, 0): inv_rot_y,
    Vector3D(0, 0, 1): rot_z,
    Vector3D(0, 0, -1): inv_rot_z,
}
"""
Axis-aligned rotation lookup map (used internally).
"""


R3D_IDENTITY: Final[Rotation3D] = Rotation3D(1, 0, 0, 0, 1, 0, 0, 0, 1)
"""
The identity rotation.
"""
