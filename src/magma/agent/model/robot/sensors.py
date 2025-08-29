from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magma.agent.communication.perception import (
    AccelerometerPerceptor,
    FreeJointPerceptor,
    GyroRatePerceptor,
    IMUPerceptor,
    JointStatePerceptor,
    Loc2DPerceptor,
    Loc3DPerceptor,
    ObjectDetection,
    Perception,
    Pos2DPerceptor,
    Pos3DPerceptor,
    Rot2DPerceptor,
    Rot3DPerceptor,
    VisionPerceptor,
)
from magma.common.math.geometry.pose import P2D_ZERO, P3D_ZERO, Pose2D, Pose3D
from magma.common.math.geometry.rotation import R3D_IDENTITY, Rotation3D
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magma.agent.model.robot.robot_tree import FreeJoint, HingeJoint


class PSensor(Protocol):
    """Protocol for sensors attached to specific body parts or joints of a robot model."""

    @property
    def name(self) -> str:
        """The name of the sensor."""

    @property
    def frame_id(self) -> str:
        """The frame-id (the name) of the body part this sensor is attached to."""

    def get_time(self) -> float:
        """Retrieve the time at which this sensor received its last update."""

    def received_update(self) -> bool:
        """Check if the sensor received new information in this update-cycle."""


class PMutableSensor(PSensor, Protocol):
    """Protocol for mutable sensors."""

    def update(self, perception: Perception) -> None:
        """Update the sensor state from the given perception.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """


@runtime_checkable
class PAccelerometer(PSensor, Protocol):
    """Protocol for accelerometer sensors."""

    def get_acc(self) -> Vector3D:
        """Retrieve the sensed linear acceleration."""


@runtime_checkable
class PGyroscope(PSensor, Protocol):
    """Protocol for gyroscope sensors."""

    def get_rpy(self) -> Vector3D:
        """Retrieve the sensed angular velocities."""


@runtime_checkable
class PIMU(PSensor, Protocol):
    """Protocol for IMU sensors."""

    def get_acc(self) -> Vector3D:
        """Retrieve the sensed linear acceleration."""

    def get_rpy(self) -> Vector3D:
        """Retrieve the sensed angular velocities."""

    def get_orientation(self) -> Rotation3D:
        """Retrieve the estimated orientation."""


@runtime_checkable
class PHingeJointSensor(PSensor, Protocol):
    """Protocol for hinge joint sensors."""

    def get_position(self) -> float:
        """Retrieve the joint position."""

    def get_velocity(self) -> float:
        """Retrieve the joint velocity."""

    def get_effort(self) -> float:
        """Retrieve the joint effort."""


@runtime_checkable
class PFreeJointSensor(PSensor, Protocol):
    """Protocol for free joint sensors."""

    def get_pose(self) -> Pose3D:
        """Retrieve the joint pose."""


@runtime_checkable
class PLoc2DSensor(PSensor, Protocol):
    """Protocol for 2D location sensors."""

    def get_loc(self) -> Pose2D:
        """Retrieve the perceived location."""


@runtime_checkable
class PLoc3DSensor(PSensor, Protocol):
    """Protocol for 3D location sensors."""

    def get_loc(self) -> Pose3D:
        """Retrieve the perceived location."""


class Sensor(ABC):
    """Base class for all sensors of a robot model."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str):
        """Construct a new sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.
        """

        super().__init__()

        self.name: Final[str] = name
        """The name of the sensor."""

        self.frame_id: Final[str] = frame_id
        """The frame-id (the name) of the body part this sensor is attached to."""

        self.perceptor_name: Final[str] = perceptor_name
        """The name of the perceptor associated with this sensor."""

        self._time: float = 0.0
        """The time this sensor received tis last update."""

        self._changed: bool = False
        """Flag indicating if new sensor information has been received in this update-cycle."""

    def get_time(self) -> float:
        """Retrieve the time at which this sensor received its last update."""

        return self._time

    def received_update(self) -> bool:
        """Check if the sensor received new information in this update-cycle."""

        return self._changed

    def set_time(self, time: float) -> None:
        """Set the sensor information timestamp and signal the availability of new sensor information.

        Parameter
        ---------
        time : float
            The sensor information time.
        """

        self._time = time
        self._changed = True

    def update(self, perception: Perception) -> None:
        """Update the sensor state from the given perception.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """

        self._changed = False

        self._update(perception)

    @abstractmethod
    def _update(self, perception: Perception) -> None:
        """Update the sensor state from the given perception.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """


class Accelerometer(Sensor):
    """Accelerometer sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str) -> None:
        """Construct a new accelerometer sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._acc: Vector3D = V3D_ZERO
        """The sensed linear acceleration."""

    def get_acc(self) -> Vector3D:
        """Retrieve the sensed linear acceleration."""

        return self._acc

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, AccelerometerPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._acc = perceptor.acceleration


class Gyroscope(Sensor):
    """Gyro rate sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str) -> None:
        """Construct a new gyro rate sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._rpy: Vector3D = V3D_ZERO
        """The sensed angular velocities."""

    def get_rpy(self) -> Vector3D:
        """Retrieve the sensed angular velocities."""

        return self._rpy

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, GyroRatePerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._rpy = perceptor.rpy


class IMU(Sensor):
    """Inertial Measurement Unit (IMU) sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str) -> None:
        """Construct a new IMU sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._orientation: Rotation3D = R3D_IDENTITY
        """The current orientation estimation."""

        self._acc: Vector3D = V3D_ZERO
        """The sensed linear acceleration."""

        self._rpy: Vector3D = V3D_ZERO
        """The sensed angular velocities."""

    def get_orientation(self) -> Rotation3D:
        """Retrieve the estimated orientation."""

        return self._orientation

    def get_acc(self) -> Vector3D:
        """Retrieve the sensed linear acceleration."""

        return self._acc

    def get_rpy(self) -> Vector3D:
        """Retrieve the sensed angular velocities."""

        return self._rpy

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, IMUPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._orientation = perceptor.orientation
            self._acc = perceptor.acc
            self._rpy = perceptor.rpy


class HingeJointSensor(Sensor):
    """Hinge joint state sensor representation."""

    def __init__(
        self,
        name: str,
        frame_id: str,
        perceptor_name: str,
        joint: HingeJoint,
    ) -> None:
        """Construct a new hinge joint state sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.

        joint : HingeJoint
            The joint associated with the joint sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self.joint: Final[HingeJoint] = joint
        """The joint associated with this joint sensor."""

        self._position: float = 0.0
        """The sensed joint position."""

        self._velocity: float = 0.0
        """The sensed joint velocity."""

        self._effort: float = 0.0
        """The sensed joint torque."""

    def get_position(self) -> float:
        """Retrieve the joint position."""

        return self._position

    def get_velocity(self) -> float:
        """Retrieve the joint velocity."""

        return self._velocity

    def get_effort(self) -> float:
        """Retrieve the joint effort."""

        return self._effort

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, JointStatePerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._position = perceptor.position
            self._velocity = perceptor.velocity
            self._effort = perceptor.effort

            self.joint.set(self._position, self._velocity, self._effort)


class FreeJointSensor(Sensor):
    """Free joint state sensor representation."""

    def __init__(
        self,
        name: str,
        frame_id: str,
        perceptor_name: str,
        joint: FreeJoint,
    ) -> None:
        """Construct a new hinge joint state sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.

        joint : FreeJoint
            The joint associated with the joint sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self.joint: Final[FreeJoint] = joint
        """The joint associated with this joint sensor."""

        self._pose: Pose3D = P3D_ZERO
        """The sensed joint pose."""

    def get_pose(self) -> Pose3D:
        """Retrieve the joint pose."""

        return self._pose

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, FreeJointPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = perceptor.pose

            self.joint.set(self._pose)


class Camera(Sensor):
    """Default camera sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str, h_fov: float, v_fov: float) -> None:
        """Construct a new camera sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.

        h_fov : float
            The horizontal field of view.

        v_fov : float
            The vertical field of view.
        """

        super().__init__(name, frame_id, perceptor_name)

        self.horizontal_fov: Final[float] = h_fov
        """The horizontal field of view."""

        self.vertical_fov: Final[float] = v_fov
        """The vertical field of view."""

    def _update(self, perception: Perception) -> None:
        del perception  # signal unused parameter


class VisionSensor(Sensor):
    """Default vision pipeline sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str, h_fov: float, v_fov: float) -> None:
        """Construct a new vision pipeline sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.

        h_fov : float
            The horizontal field of view.

        v_fov : float
            The vertical field of view.
        """

        super().__init__(name, frame_id, perceptor_name)

        self.horizontal_fov: Final[float] = h_fov
        """The horizontal field of view."""

        self.vertical_fov: Final[float] = v_fov
        """The vertical field of view."""

        self._objects: Sequence[ObjectDetection] = []
        """The collection of point object detections."""

    def get_object_detections(self) -> Sequence[ObjectDetection]:
        """Return the collection of most recent object detections."""

        return self._objects

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, VisionPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._objects = perceptor.objects


class Loc2DSensor(Sensor):
    """Default 2D location sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_prefix: str) -> None:
        """Construct a new 2D location sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_prefix : str
            The naming prefix of the perceptor associated with the sensor.
        """

        super().__init__(name, frame_id, perceptor_prefix)

        self._pose: Pose2D = P2D_ZERO

    def get_loc(self) -> Pose2D:
        """Retrieve the perceived location information."""

        return self._pose

    def _update(self, perception: Perception) -> None:
        # try updating using location perceptor
        perceptor = perception.get_perceptor(self.perceptor_name, Loc2DPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = perceptor.loc
            return

        # try updating using individual position and orientation perceptors
        pos_perceptor = perception.get_perceptor(self.perceptor_name + '_pos', Pos2DPerceptor)
        rot_perceptor = perception.get_perceptor(self.perceptor_name + '_theta', Rot2DPerceptor)

        if pos_perceptor is not None and rot_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = Pose2D(pos_perceptor.pos, rot_perceptor.theta)

        elif pos_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = Pose2D(pos_perceptor.pos, self._pose.theta)

        elif rot_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = Pose2D(self._pose.pos, rot_perceptor.theta)


class Loc3DSensor(Sensor):
    """Default 3D location sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_prefix: str) -> None:
        """Construct a new 3D location sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_prefix : str
            The naming prefix of the perceptor associated with the sensor.
        """

        super().__init__(name, frame_id, perceptor_prefix)

        self._pose: Pose3D = P3D_ZERO

    def get_location(self) -> Pose3D:
        """Retrieve the perceived location information."""

        return self._pose

    def _update(self, perception: Perception) -> None:
        # try updating using location perceptor
        loc_perceptor = perception.get_perceptor(self.perceptor_name + '_loc', Loc3DPerceptor)

        if loc_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = loc_perceptor.loc
            return

        # try updating using individual position and orientation perceptors
        pos_perceptor = perception.get_perceptor(self.perceptor_name + '_pos', Pos3DPerceptor)
        rot_perceptor = perception.get_perceptor(self.perceptor_name + '_quat', Rot3DPerceptor)

        if pos_perceptor is not None and rot_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = Pose3D(pos_perceptor.pos, rot_perceptor.rot)

        elif pos_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = Pose3D(pos_perceptor.pos, self._pose.rot)

        elif rot_perceptor is not None:
            self.set_time(perception.get_time())
            self._pose = Pose3D(self._pose.pos, rot_perceptor.rot)
