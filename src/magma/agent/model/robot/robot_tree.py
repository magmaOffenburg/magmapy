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
    """Protocol for joints connecting body parts of a robot model."""

    @property
    def name(self) -> str:
        """The name of the joint."""

    @property
    def anchor(self) -> Vector3D:
        """The joint anchor."""

    def get_rotation(self) -> Rotation3D:
        """Retrieve the current 3D rotation of the joint in the joint local frame."""

    def get_translation(self) -> Vector3D:
        """Retrieve the current 3D translation of the joint in the joint local frame."""

    def get_transform(self) -> Pose3D:
        """Retrieve the current 3D transformation of the joint in the joint local frame (translation and rotation)."""


@runtime_checkable
class PFixedJoint(PJoint, Protocol):
    """Protocol for hinge joints."""


@runtime_checkable
class PHingeJoint(PJoint, Protocol):
    """Protocol for hinge joints."""

    @property
    def axis(self) -> Vector3D:
        """The joint rotation axis."""

    def ax_min(self) -> float:
        """The minimum possible joint position."""

    def ax_max(self) -> float:
        """The maximum possible joint position."""


@runtime_checkable
class PFreeJoint(PJoint, Protocol):
    """Protocol for hinge joints."""

    def get_pose(self) -> Pose3D:
        """Retrieve the joint pose."""


class PBodyPart(Protocol):
    """Protocol for body part representations."""

    @property
    def name(self) -> str:
        """The name of the body part."""

    def parent(self) -> PBodyPart | None:
        """Retrieve the parent body part (if existing)."""

    @property
    def children(self) -> Sequence[PBodyPart]:
        """The collection of child body parts."""

    @property
    def inertia(self) -> RigidBodyInertia:
        """The body part inertia."""

    @property
    def joint(self) -> Joint | None:
        """The joint by which this body part is attached to its parent body part (if existing)."""

    @property
    def appearance(self) -> BodyVisual | None:
        """The body part visual appearance."""

    def is_root_body(self) -> bool:
        """Check if this body part represents the root body part of the robot."""

    def get_pose(self) -> Pose3D:
        """Calculate the current pose of the body part in the robot frame."""


class Joint:
    """Base class for all joints of a robot model."""

    def __init__(self, name: str, anchor: Vector3D) -> None:
        """Construct a new joint.

        Parameter
        ---------
        name : str
            The unique name of the joint.

        anchor : Vector3D
            The joint anchor (position in the parent frame).
        """

        self.name: Final[str] = name
        """The unique name of the joint."""

        self.anchor: Final[Vector3D] = anchor
        """The joint anchor (position in the parent frame)."""

        self._translation: Vector3D = anchor
        """The translation induced by the joint."""

        self._rotation: Rotation3D = R3D_IDENTITY
        """The rotation induced by the joint."""

    def get_rotation(self) -> Rotation3D:
        """Retrieve the current 3D rotation of the joint in the joint local frame."""

        return self._rotation

    def get_translation(self) -> Vector3D:
        """Retrieve the current 3D translation of the joint in the joint local frame."""

        return self._translation

    def get_transform(self) -> Pose3D:
        """Retrieve the current 3D transformation of the joint in the joint local frame (translation and rotation)."""

        return Pose3D(self._translation, self._rotation)


class FixedJoint(Joint):
    """Default fixed joint implementation."""

    def __init__(self, name: str, anchor: Vector3D, orientation: Rotation3D) -> None:
        """Construct a new joint.

        Parameter
        ---------
        name : str
            The unique name of the joint.

        anchor : Vector3D
            The joint anchor (position in the parent frame).

        orientation : Rotation3D
            The fixed orientation of the joint.
        """

        super().__init__(name, anchor)

        self._rotation = orientation


class HingeJoint(Joint):
    """Default hinge joint implementation."""

    def __init__(self, name: str, anchor: Vector3D, axis: Vector3D, limits: Vector2D) -> None:
        """Construct a new hinge joint.

        Parameter
        ---------
        name : str
            The unique name of the joint.

        anchor : Vector3D
            The joint anchor (position in the parent frame).

        axis : Vector3D
            The hinge joint rotation axis.

        limits : Vector2D
            The joint limits (minimum / maximum joint angle)
        """

        super().__init__(name, anchor)

        self.axis: Final[Vector3D] = axis
        """The joint rotation axis."""

        self.limits: Final[Vector2D] = limits
        """The minimum and maximum joint angles."""

        self._ax_position: float = 0.0
        """The current joint axis position."""

        self._ax_velocity: float = 0.0
        """The current joint axis velocity."""

        self._ax_effort: float = 0.0
        """The current joint axis torque."""

    def set(self, pos: float, vel: float, effort: float) -> None:
        """Set the joint state.

        Parameter
        ---------
        pos : float
            The current joint axis position.

        vel : float
            The current joint axis velocity.

        effort : float
            The current joint axis torque.
        """

        self._ax_position = pos
        self._ax_velocity = vel
        self._ax_effort = effort

        # update rotation information
        self._rotation = axis_angle(self.axis, self._ax_position)

    def ax_min(self) -> float:
        """The minimum possible joint position."""

        return self.limits.x

    def ax_max(self) -> float:
        """The maximum possible joint position."""

        return self.limits.y

    def ax_pos(self) -> float:
        """Retrieve the joint axis position."""

        return self._ax_position

    def ax_vel(self) -> float:
        """Retrieve the joint axis velocity."""

        return self._ax_velocity

    def ax_effort(self) -> float:
        """Retrieve the joint axis effort."""

        return self._ax_effort


class FreeJoint(Joint):
    """Default free joint implementation."""

    def __init__(self, name: str, anchor: Vector3D) -> None:
        """Construct a new free joint.

        Parameter
        ---------
        name : str
            The unique name of the joint.

        anchor : Vector3D
            The joint anchor (position in the parent frame).
        """

        super().__init__(name, anchor)

        self._pose: Pose3D = P3D_ZERO
        """The current joint pose (sensed translation and rotation)"""

    def set(self, pose: Pose3D) -> None:
        """Set the joint state."""

        self._pose = pose

        # update joint rotation and translation information
        self._rotation = pose.rot
        self._translation = self.anchor + pose.pos

    def joint_pose(self) -> Pose3D:
        """Retrieve the joint pose."""

        return self._pose


class RigidBodyInertia:
    """Default inertia representation for a rigid body part."""

    def __init__(
        self,
        origin: Vector3D,
        mass: float,
        inertia: Vector3D,
    ) -> None:
        """Construct a new body inertia.

        Parameter
        ---------
        origin : Vector3D
            The inertia origin / center of mass.

        mass : float
            The body mass.

        inertia : Vector3D
            The (diagonal) inertia parameter.
        """

        self.origin: Final[Vector3D] = origin
        self.mass: Final[float] = mass
        self.inertia: Final[Vector3D] = inertia


ZERO_INERTIA: Final[RigidBodyInertia] = RigidBodyInertia(V3D_ZERO, 0, V3D_ZERO)
"""The zero rigid body inertia with no mass and zero inertia."""


class BodyVisual:
    """Default body visual representation."""

    def __init__(
        self,
        origin: Vector3D,
        dimensions: Vector3D,
    ) -> None:
        """Construct a new body inertia.

        Parameter
        ---------
        origin : Vector3D
            The origin of the visual representation relative to the body frame.

        dimensions : Vector3D
            The visuals bounding box dimensions.
        """

        self.origin: Final[Vector3D] = origin
        """The origin of the visual representation."""

        self.dimensions: Final[Vector3D] = dimensions
        """The dimensions of the bounding box."""


class BodyPart:
    """Default representation of a body part."""

    def __init__(
        self,
        name: str,
        children: Sequence[BodyPart],
        inertia: RigidBodyInertia,
        joint: Joint | None,
        appearance: BodyVisual | None,
    ) -> None:
        """Construct a new body part.

        Parameter
        ---------
        name : str
            The unique name of the body part.

        children : Sequence[BodyPart]
            The collection of child body parts.

        inertia : RigidBodyInertia
            The body inertia.

        joint : Joint | None
            The joint attaching the body to its parent.

        appearance : BodyVisual | None
            The visual appearance of the body.
        """

        self.name: Final[str] = name
        """The unique name of the body part."""

        self.children: Final[Sequence[BodyPart]] = children
        """The collection of child body parts."""

        self.inertia: Final[RigidBodyInertia] = inertia
        """The body part inertia."""

        self.joint: Final[Joint | None] = joint
        """The joint attaching this body part to its parent."""

        self.appearance: Final[BodyVisual | None] = appearance
        """The visual appearance of the body."""

        self._parent: BodyPart | None = None
        """The parent body part."""

        # set parent references of child body parts
        for child in children:
            # object.__setattr__(child, '_parent', self)
            child._parent = self  # noqa: SLF001 - prevent private member access warning for instances of the same class

    def parent(self) -> BodyPart | None:
        """Retrieve the parent body part (if existing)."""

        return self._parent

    def is_root_body(self) -> bool:
        """Check if this body part represents the root body part of the robot."""

        return self._parent is None or self.joint is None

    def get_pose(self) -> Pose3D:
        """Calculate the current pose of the body part in the robot frame."""

        if self._parent is None:
            # root body part -> zero pose
            return P3D_ZERO

        if self.joint is None:
            # should not happen, as the root body without a parent body should be the only body with no joint reference
            return self._parent.get_pose()

        return self._parent.get_pose().tf_pose(self.joint.get_transform())

    def get_body(self, name: str) -> BodyPart | None:
        """Return the body with the given name."""

        # check this body part
        if self.name == name:
            return self

        # check child bodies
        for child in self.children:
            body = child.get_body(name)
            if body is not None:
                return body

        return None

    def count_bodies(self) -> int:
        """Recursively count the number of bodies (including this body part)."""

        n_bodies = 1

        for child in self.children:
            n_bodies += child.count_bodies()

        return n_bodies
