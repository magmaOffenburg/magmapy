from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magma.common.math.geometry.pose import P3D_ZERO, Pose3D
from magma.common.math.geometry.rotation import R3D_IDENTITY, Rotation3D, axis_angle
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magma.common.math.geometry.vector import Vector2D


@runtime_checkable
class PJoint(Protocol):
    """
    Protocol for joints connecting body parts of a robot model.
    """

    @property
    def name(self) -> str:
        """
        The name of the joint.
        """

    @property
    def anchor(self) -> Vector3D:
        """
        The joint anchor.
        """

    def get_rotation(self) -> Rotation3D:
        """
        Retrieve the current 3D rotation of the joint in the joint local frame.
        """

    def get_translation(self) -> Vector3D:
        """
        Retrieve the current 3D translation of the joint in the joint local frame.
        """


@runtime_checkable
class PFixedJoint(PJoint, Protocol):
    """
    Protocol for hinge joints.
    """


@runtime_checkable
class PHingeJoint(PJoint, Protocol):
    """
    Protocol for hinge joints.
    """

    @property
    def axis(self) -> Vector3D:
        """
        The joint rotation axis.
        """

    def ax_min(self) -> float:
        """
        The minimum possible joint position.
        """

    def ax_max(self) -> float:
        """
        The maximum possible joint position.
        """


@runtime_checkable
class PFreeJoint(PJoint, Protocol):
    """
    Protocol for hinge joints.
    """

    def get_pose(self) -> Pose3D:
        """
        Retrieve the joint pose.
        """


class PBodyPart(Protocol):
    """
    Protocol for body part representations.
    """

    @property
    def name(self) -> str:
        """
        The name of the body part.
        """

    def parent(self) -> PBodyPart | None:
        """
        Retrieve the parent body part (if existing).
        """

    @property
    def children(self) -> Sequence[PBodyPart]:
        """
        The collection of child body parts.
        """

    @property
    def joint(self) -> Joint | None:
        """
        The joint by which this body part is attached to its parent body part (if existing).
        """


class Joint:
    """
    Base class for all joints of a robot model.
    """

    def __init__(self, name: str, anchor: Vector3D) -> None:
        """
        Construct a new joint.
        """

        self.name: Final[str] = name
        self.anchor: Final[Vector3D] = anchor

        self._translation: Vector3D = V3D_ZERO
        self._rotation: Rotation3D = R3D_IDENTITY

    def get_rotation(self) -> Rotation3D:
        """
        Retrieve the current 3D rotation of the joint in the joint local frame.
        """

        return self._rotation

    def get_translation(self) -> Vector3D:
        """
        Retrieve the current 3D translation of the joint in the joint local frame.
        """

        return self._translation


class FixedJoint(Joint):
    """
    Default fixed joint implementation.
    """

    def __init__(self, name: str, anchor: Vector3D, orientation: Rotation3D) -> None:
        """
        Construct a new joint.
        """

        super().__init__(name, anchor)

        self._rotation = orientation


class HingeJoint(Joint):
    """
    Default hinge joint implementation.
    """

    def __init__(self, name: str, anchor: Vector3D, axis: Vector3D, limits: Vector2D) -> None:
        """
        Construct a new hinge joint.
        """

        super().__init__(name, anchor)

        self.axis: Final[Vector3D] = axis
        self.limits: Final[Vector2D] = limits

        self._ax_position: float = 0.0
        self._ax_velocity: float = 0.0
        self._ax_effort: float = 0.0

    def set(self, pos: float, vel: float, effort: float) -> None:
        """
        Set the joint state.
        """

        self._ax_position = pos
        self._ax_velocity = vel
        self._ax_effort = effort

        # update rotation information
        self._rotation = axis_angle(self.axis, self._ax_position)

    def ax_min(self) -> float:
        """
        The minimum possible joint position.
        """

        return self.limits.x

    def ax_max(self) -> float:
        """
        The maximum possible joint position.
        """

        return self.limits.y

    def ax_pos(self) -> float:
        """
        Retrieve the joint axis position.
        """

        return self._ax_position

    def ax_vel(self) -> float:
        """
        Retrieve the joint axis velocity.
        """

        return self._ax_velocity

    def ax_effort(self) -> float:
        """
        Retrieve the joint axis effort.
        """

        return self._ax_effort


class FreeJoint(Joint):
    """
    Default free joint implementation.
    """

    def __init__(self, name: str, anchor: Vector3D) -> None:
        """
        Construct a new free joint.
        """

        super().__init__(name, anchor)

        self._pose: Pose3D = P3D_ZERO

    def set(self, pose: Pose3D) -> None:
        """
        Set the joint state.
        """

        self._pose = pose

        # update joint rotation and translation information
        self._rotation = pose.rot
        self._translation = pose.pos

    def joint_pose(self) -> Pose3D:
        """
        Retrieve the joint pose.
        """

        return self._pose


class BodyPart:
    """
    Default representation of a body part.
    """

    def __init__(
        self,
        name: str,
        children: Sequence[BodyPart],
        position: Vector3D,
        joint: Joint | None,
    ) -> None:
        """
        Construct a new body part.
        """

        self.name: Final[str] = name
        self.children: Final[Sequence[BodyPart]] = children
        self.position: Final[Vector3D] = position
        self.joint: Final[Joint | None] = joint

        self._parent: BodyPart | None = None

        # set parent references of child body parts
        for child in children:
            # object.__setattr__(child, '_parent', self)
            child._parent = self  # noqa: SLF001 - prevent private member access warning for instances of the same class

    def parent(self) -> BodyPart | None:
        """
        Retrieve the parent body part (if existing).
        """

        return self._parent

    def is_root_body(self) -> bool:
        """
        Check if this body part represents the root body part of the robot.
        """

        return self.joint is None
