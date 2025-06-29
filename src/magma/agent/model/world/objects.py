from __future__ import annotations

from typing import Final, Protocol

from magma.common.math.geometry.angle import Angle2D, angle_to_xy
from magma.common.math.geometry.pose import Pose2D, Pose3D
from magma.common.math.geometry.rotation import R3D_IDENTITY, Rotation3D
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D
from magma.common.util.map.feature.features import PLineFeature, PPointFeature


class PVisibleObject(Protocol):
    """Protocol for visible objects in the world."""

    @property
    def name(self) -> str:
        """The unique name of the visible object."""

    def get_position(self) -> Vector3D:
        """Return the estimated position of the visible object."""

    def get_orientation(self) -> Rotation3D:
        """Return the estimated orientation of the object."""

    def get_horizontal_angle(self) -> Angle2D:
        """Return the estimated horizontal angle of the object."""

    def get_pose(self) -> Pose3D:
        """Return the pose of the object."""

    def get_pose_2d(self) -> Pose2D:
        """Return the 2D projected pose of the object."""

    def distance_to(self, other: PVisibleObject) -> float:
        """Calculate the 3D distance to the other object.

        Parameter
        ---------
        other : PVisibleObject
            The object to which to calculate the distance.
        """

    def distance_to_2d(self, other: PVisibleObject) -> float:
        """Calculate the 2D distance to the other object.

        Parameter
        ---------
        other : PVisibleObject
            The object to which to calculate the distance.
        """


class PMovableObject(PVisibleObject, Protocol):
    """Protocol for movable objects in the world."""

    def get_velocity(self) -> Vector3D:
        """Return the estimated velocity of the object."""


class PPointLandmark(PVisibleObject, PPointFeature, Protocol):
    """Protocol for point landmarks in the world."""


class PLineLandmark(PVisibleObject, PLineFeature, Protocol):
    """Protocol for line segment landmarks in the world."""

    def get_position1(self) -> Vector3D:
        """Return the first estimated position of the line segment landmark."""

    def get_position2(self) -> Vector3D:
        """Return the second estimated position of the line segment landmark."""


class VisibleObject:
    """Representation of a visible object in the world."""

    def __init__(
        self,
        name: str,
        position: Vector3D | None = None,
        orientation: Rotation3D | None = None,
    ) -> None:
        """Construct a new visible object.

        Parameter
        ---------
        name : str
            The unique name of the object.

        position : Vector3D | None, default=None
            The initial global position of the object.
            If ``None``, the global position is initialized to zero.

        orientation : Rotation3D | None, default=None
            The initial global orientation of the object.
            If ``None``, the global orientation is initialized to the identity.
        """

        self.name: Final[str] = name
        """The unique name used to identify the object."""

        self._position: Vector3D = V3D_ZERO if position is None else position
        """The global position of the object."""

        self._orientation: Rotation3D = R3D_IDENTITY if orientation is None else orientation
        """The global orientation of the object."""

    def get_position(self) -> Vector3D:
        """Return the estimated position of the visible object."""

        return self._position

    def get_orientation(self) -> Rotation3D:
        """Return the estimated orientation of the object."""

        return self._orientation

    def get_horizontal_angle(self) -> Angle2D:
        """Return the estimated horizontal angle of the object."""

        return angle_to_xy(self._orientation.m11, self._orientation.m21)

    def get_pose(self) -> Pose3D:
        """Return the pose of the object."""

        return Pose3D(self._position, self._orientation)

    def get_pose_2d(self) -> Pose2D:
        """Return the 2D projected pose of the object."""

        return Pose2D(self._position.as_2d(), self.get_horizontal_angle())

    def distance_to(self, other: PVisibleObject) -> float:
        """Calculate the 3D distance to the other object.

        Parameter
        ---------
        other : PVisibleObject
            The object to which to calculate the distance.
        """

        return (self._position - other.get_position()).norm()

    def distance_to_2d(self, other: PVisibleObject) -> float:
        """Calculate the 2D distance to the other object.

        Parameter
        ---------
        other : PVisibleObject
            The object to which to calculate the distance.
        """

        return (self._position.as_2d() - other.get_position().as_2d()).norm()


class MovableObject(VisibleObject):
    """Representation of a movable object in the world."""

    def __init__(
        self,
        name: str,
        position: Vector3D | None = None,
        orientation: Rotation3D | None = None,
    ) -> None:
        """Construct a new movable object.

        Parameter
        ---------
        name : str
            The unique name of the object.

        position : Vector3D | None, default=None
            The initial global position of the object.
            If ``None``, the global position is initialized to zero.

        orientation : Rotation3D | None, default=None
            The initial global orientation of the object.
            If ``None``, the global orientation is initialized to the identity.
        """

        super().__init__(name, position, orientation)

        self._velocity: Vector3D = V3D_ZERO
        """The global linear velocity of the object."""

    def get_velocity(self) -> Vector3D:
        """Return the estimated velocity of the object."""

        return self._velocity


class Landmark(VisibleObject):
    """Representation of a static landmark object in the world."""

    def __init__(
        self,
        name: str,
        lm_type: str,
        position: Vector3D | None = None,
        orientation: Rotation3D | None = None,
    ) -> None:
        """Construct a new landmark object.

        Parameter
        ---------
        name : str
            The unique name of the landmark.

        lm_type : str
            The landmark type.

        position : Vector3D | None, default=None
            The initial global position of the object.
            If ``None``, the global position is initialized to zero.

        orientation : Rotation3D | None, default=None
            The initial global orientation of the object.
            If ``None``, the global orientation is initialized to the identity.
        """

        super().__init__(name, position, orientation)

        self.lm_type: Final[str] = lm_type
        """The type of landmark."""

    def get_type(self) -> str:
        """Return he type of landmark."""

        return self.lm_type


class PointLandmark(Landmark):
    """Representation of a static, punctual landmark object in the world."""

    def __init__(
        self,
        name: str,
        l_type: str,
        known_position: Vector3D,
        position: Vector3D | None = None,
        orientation: Rotation3D | None = None,
    ) -> None:
        """Construct a new point landmark object.

        Parameter
        ---------
        name : str
            The unique name of the landmark.

        lm_type : str
            The landmark type.

        known_position : Vector3D
            The known fixed global position of the object.

        position : Vector3D | None, default=None
            The initial global position of the object.
            If ``None``, the global position is initialized to zero.

        orientation : Rotation3D | None, default=None
            The initial global orientation of the object.
            If ``None``, the global orientation is initialized to the identity.
        """

        super().__init__(name, l_type, position, orientation)

        self._known_position: Vector3D = known_position
        """The known position of this point landmark."""

    def get_known_position(self) -> Vector3D:
        """Return the known position of this point landmark."""

        return self._known_position


class LineLandmark(Landmark):
    """Representation of a static, line segment landmark object in the world."""

    def __init__(
        self,
        name: str,
        l_type: str,
        known_position1: Vector3D,
        known_position2: Vector3D,
        position1: Vector3D | None = None,
        position2: Vector3D | None = None,
    ) -> None:
        """Construct a new line segment landmark object.

        Parameter
        ---------
        name : str
            The unique name of the landmark.

        lm_type : str
            The landmark type.

        known_position1 : Vector3D
            The first known fixed global position of the line segment.

        known_position2 : Vector3D
            The second known fixed global position of the line segment.

        position1 : Vector3D | None, default=None
            The initial first global position of the line segment.
            If ``None``, the first global position is initialized to zero.

        position2 : Vector3D | None, default=None
            The initial second global position of the line segment.
            If ``None``, the second global position is initialized to zero.
        """

        super().__init__(name, l_type)

        self._position1: Vector3D = V3D_ZERO if position1 is None else position1
        """The first global position of the line segment."""

        self._position2: Vector3D = V3D_ZERO if position2 is None else position2
        """The second global position of the line segment."""

        self._known_position1: Vector3D = known_position1
        """The first known position of this line segment landmark."""

        self._known_position2: Vector3D = known_position2
        """The second known position of this line segment landmark."""

        self._update_line_pose()

    def _update_line_pose(self) -> None:
        """Update the object position and orientation based on estimated line segment endpoints."""

        if self._position1 == self._position2:
            self._position = self._position1
            self._orientation = R3D_IDENTITY
        else:
            self._position = (self._position1 + self._position2) / 2
            # TODO: calculate orientation using XYZ rotations with a zero X rotation
            # self._orientation = R_y + R_z

    def get_position1(self) -> Vector3D:
        """Return the first estimated position of the line segment landmark."""

        return self._position

    def get_position2(self) -> Vector3D:
        """Return the second estimated position of the line segment landmark."""

        return self._position

    def get_known_position1(self) -> Vector3D:
        """Return the first known position of this line segment landmark."""

        return self._known_position1

    def get_known_position2(self) -> Vector3D:
        """Return the second known position of this line segment landmark."""

        return self._known_position2
