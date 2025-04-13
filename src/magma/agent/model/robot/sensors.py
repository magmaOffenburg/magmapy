from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from magma.agent.communication.perception import (
    AccelerometerPerceptor,
    FreeJointPerceptor,
    GyroRatePerceptor,
    IMUPerceptor,
    JointStatePerceptor,
    Perception,
)
from magma.common.math.geometry.pose import Pose3D
from magma.common.math.geometry.rotation import Rotation3D
from magma.common.math.geometry.vector import Vector3D

if TYPE_CHECKING:
    from magma.agent.model.robot.robot_tree import FreeJoint, HingeJoint


class PSensor(Protocol):
    """
    Protocol for sensors attached to specific body parts or joints of a robot model.
    """

    def get_name(self) -> str:
        """
        Retrieve the name of the sensor.
        """

    def get_frame_id(self) -> str:
        """
        Retrieve the frame-id (the name) of the body part this sensor is attached to.
        """

    def get_time(self) -> float:
        """
        Retrieve the time at which this sensor received its last update.
        """


class PMutableSensor(PSensor, Protocol):
    """
    Protocol for mutable sensors.
    """

    def update(self, perception: Perception) -> None:
        """
        Update the sensor state from the given perception.
        """


@runtime_checkable
class PAccelerometer(PSensor, Protocol):
    """
    Protocol for accelerometer sensors.
    """

    def get_acc(self) -> Vector3D:
        """
        Retrieve the sensed linear acceleration.
        """


@runtime_checkable
class PGyroscope(PSensor, Protocol):
    """
    Protocol for gyroscope sensors.
    """

    def get_rpy(self) -> Vector3D:
        """
        Retrieve the sensed angular velocities.
        """


@runtime_checkable
class PIMU(PSensor, Protocol):
    """
    Protocol for IMU sensors.
    """

    def get_acc(self) -> Vector3D:
        """
        Retrieve the sensed linear acceleration.
        """

    def get_rpy(self) -> Vector3D:
        """
        Retrieve the sensed angular velocities.
        """

    def get_orientation(self) -> Rotation3D:
        """
        Retrieve the estimated orientation.
        """


@runtime_checkable
class PHingeJointSensor(PSensor, Protocol):
    """
    Protocol for hinge joint sensors.
    """

    def get_position(self) -> float:
        """
        Retrieve the joint position.
        """

    def get_velocity(self) -> float:
        """
        Retrieve the joint velocity.
        """

    def get_effort(self) -> float:
        """
        Retrieve the joint effort.
        """


@runtime_checkable
class PFreeJointSensor(PSensor, Protocol):
    """
    Protocol for free joint sensors.
    """

    def get_pose(self) -> Pose3D:
        """
        Retrieve the joint pose.
        """


class Sensor(ABC):
    """
    Base class for all sensors of a robot model.
    """

    def __init__(self,
                 name: str,
                 parent: str,
                 perceptor_name: str):
        """
        Construct a new sensor.
        """

        super().__init__()

        self._name: str = name
        self._frame_id: str = parent
        self._time: float = 0.0
        self._perceptor_name: str = perceptor_name

    def get_name(self) -> str:
        """
        Retrieve the name of the sensor.
        """

        return self._name

    def get_frame_id(self) -> str:
        """
        Retrieve the frame-id (the name) of the body part this sensor is attached to.
        """

        return self._frame_id

    def get_time(self) -> float:
        """
        Retrieve the time at which this sensor received its last update.
        """

        return self._time

    @abstractmethod
    def update(self, perception: Perception) -> None:
        """
        Update the sensor state from the given perception.
        """


class Accelerometer(Sensor):
    """
    Accelerometer sensor representation.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str) -> None:
        """
        Construct a new accelerometer sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._acc: Vector3D = Vector3D()

    def get_acc(self) -> Vector3D:
        """
        Retrieve the sensed acceleration.
        """

        return self._acc

    def update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self._perceptor_name, AccelerometerPerceptor)

        if perceptor is not None:
            self._time = perception.get_time()
            self._acc = perceptor.acceleration


class Gyroskope(Sensor):
    """
    Gyro rate sensor representation.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str) -> None:
        """
        Construct a new gyro rate sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._rpy: Vector3D = Vector3D()

    def get_rpy(self) -> Vector3D:
        """
        Retrieve the sensed angular velocities.
        """

        return self._rpy

    def update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self._perceptor_name, GyroRatePerceptor)

        if perceptor is not None:
            self._time = perception.get_time()
            self._rpy = perceptor.rpy


class IMU(Sensor):
    """
    Inertial Measurement Unit (IMU) sensor representation.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str) -> None:
        """
        Construct a new IMU sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._orientation: Rotation3D = Rotation3D()
        self._acc: Vector3D = Vector3D()
        self._rpy: Vector3D = Vector3D()

    def get_orientation(self) -> Rotation3D:
        """
        Retrieve the estimated orientation.
        """

        return self._orientation

    def get_acc(self) -> Vector3D:
        """
        Retrieve the sensed linear acceleration.
        """

        return self._acc

    def get_rpy(self) -> Vector3D:
        """
        Retrieve the sensed angular velocities.
        """

        return self._rpy

    def update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self._perceptor_name, IMUPerceptor)

        if perceptor is not None:
            self._time = perception.get_time()
            self._orientation = perceptor.orientation
            self._acc = perceptor.acc
            self._rpy = perceptor.rpy


class HingeJointSensor(Sensor):
    """
    Hinge joint state sensor representation.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str,
                 joint: HingeJoint) -> None:
        """
        Construct a new hinge joint state sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._joint: HingeJoint = joint

        self._position: float = 0.0
        self._velocity: float = 0.0
        self._effort: float = 0.0

    def get_position(self) -> float:
        """
        Retrieve the joint position.
        """

        return self._position

    def get_velocity(self) -> float:
        """
        Retrieve the joint velocity.
        """

        return self._velocity

    def get_effort(self) -> float:
        """
        Retrieve the joint effort.
        """

        return self._effort

    def update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self._perceptor_name, JointStatePerceptor)

        if perceptor is not None:
            self._time = perception.get_time()
            self._position = perceptor.position
            self._velocity = perceptor.velocity
            self._effort = perceptor.effort

            self._joint.set(self._position, self._velocity, self._effort)


class FreeJointSensor(Sensor):
    """
    Free joint state sensor representation.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str,
                 joint: FreeJoint) -> None:
        """
        Construct a new hinge joint state sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._joint: FreeJoint = joint

        self._pose: Pose3D = Pose3D()

    def get_pose(self) -> Pose3D:
        """
        Retrieve the joint pose.
        """

        return self._pose

    def update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self._perceptor_name, FreeJointPerceptor)

        if perceptor is not None:
            self._time = perception.get_time()
            self._pose = perceptor.pose

            self._joint.set(self._pose)
