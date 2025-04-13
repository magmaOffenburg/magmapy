from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from magma.common.math.geometry.pose import Pose3D
from magma.common.math.geometry.rotation import Rotation3D
from magma.common.math.geometry.vector import Vector3D

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magma.common.math.geometry.vector import Vector2D


@runtime_checkable
class PJoint(Protocol):
    """
    Protocol for joints connecting body parts of a robot model.
    """

    def get_name(self) -> str:
        """
        Retrieve the name of the joint.
        """

    def get_anchor(self) -> Vector3D:
        """
        Retrieve the joint anchor.
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

    def get_axis(self) -> Vector3D:
        """
        Retrieve the joint axis.
        """

    def get_min(self) -> float:
        """
        Retrieve the minimum possible joint position.
        """

    def get_max(self) -> float:
        """
        Retrieve the maximum possible joint position.
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

    def get_name(self) -> str:
        """
        Retrieve the name of the body part.
        """

    def get_parent(self) -> PBodyPart | None:
        """
        Retrieve the parent body part (if existing).
        """

    def get_children(self) -> Sequence[PBodyPart]:
        """
        Retrieve the collection of child body parts.
        """

    def get_joint(self) -> Joint | None:
        """
        Retrieve the joint by which this body part is attached to its parent body part (if existing).
        """


class Joint:
    """
    Base class for all joints of a robot model.
    """

    def __init__(self, name: str, anchor: Vector3D) -> None:
        """
        Construct a new joint.
        """

        self._name = name
        self._anchor: Vector3D = anchor
        self._translation: Vector3D = Vector3D()
        self._rotation: Rotation3D = Rotation3D()

    def get_name(self) -> str:
        """
        Retrieve the name of the joint.
        """

        return self._name

    def get_anchor(self) -> Vector3D:
        """
        Retrieve the joint anchor.
        """

        return self._anchor

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

        self._axis: Vector3D = axis
        self._limits: Vector2D = limits

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
        # self._rotation = Rotation3D.from_axis_angle(self._axis, self._ax_position)

    def get_axis(self) -> Vector3D:
        """
        Retrieve the joint axis.
        """

        return self._axis

    def get_min(self) -> float:
        """
        Retrieve the minimum possible joint position.
        """

        return self._limits.x()

    def get_max(self) -> float:
        """
        Retrieve the maximum possible joint position.
        """

        return self._limits.y()

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

        self._pose: Pose3D = Pose3D()

    def set(self, pose: Pose3D) -> None:
        """
        Set the joint state.
        """

        self._pose = pose

        # update joint rotation and translation information
        self._rotation = pose.orientation()
        self._translation = pose.position()

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

        self._name: str = name
        self._parent: BodyPart | None = None
        self._children: Sequence[BodyPart] = children
        self._position: Vector3D = position
        self._joint: Joint | None = joint

        # set parent references of child body parts
        for child in children:
            child._parent = self  # noqa: SLF001 - prevent private member access warning for instances of the same class

    def get_name(self) -> str:
        """
        Retrieve the name of the body part.
        """

        return self._name

    def get_parent(self) -> BodyPart | None:
        """
        Retrieve the parent body part (if existing).
        """

        return self._parent

    def get_children(self) -> Sequence[BodyPart]:
        """
        Retrieve the collection of child body parts.
        """

        return self._children

    def get_joint(self) -> Joint | None:
        """
        Retrieve the joint by which this body part is attached to its parent body part (if existing).
        """

        return self._joint

    def get_position(self) -> Vector3D:
        """
        Retrieve the current position of the body part in the local robot frame.
        """

        return self._position

    def is_root_body(self) -> bool:
        """
        Check if this body part represents the root body part of the robot.
        """

        return self._joint is None
