from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Protocol

from magma.common.math.geometry.rotation import Rotation3D

if TYPE_CHECKING:
    from collections.abc import Generator, ValuesView

    from magma.common.math.geometry.vector import Vector2D, Vector3D


class SensorType(Enum):
    GYRO = "gyro"
    """
    A gyro rate sensor, receiving rotational velocity information.
    """

    ACCELEROMETER = "accelerometer"
    """
    An accelerometer sensor, receiving linear accelerations.
    """

    IMU = "imu"
    """
    An IMU sensor, receiving rotational velocity as well as linear acceleration information together with an orientation prediction.
    """

    CAMERA = "camera"
    """
    A camera sensor, receiving various state information about visible objects in the environment.
    """


class ActuatorType(Enum):
    LIGHT = "light"
    """
    A light that can be regulated in brightness.
    """

    RGB_LIGHT = "rgb_light"
    """
    A light that can be regulated in brightness as well as in color.
    """


class JointType(Enum):
    FIXED = "fixed"
    """
    A fixed joint, allowing no movement freedom (0DOF).
    """

    HINGE = "hinge"
    """
    A hinge joint, allowing 1DOF along one axis.
    """

    FREE = "free"
    """
    A free joint, allowing full 6DOF translational as well as rotational freedom.
    """


class PRobotDescription(Protocol):
    """
    Protocol for robot descriptions.
    """

    def get_name(self) -> str:
        """
        Retrieve the name of the robot model.
        """

    def get_root_body(self) -> BodyDescription:
        """
        Retrieve the root body part.
        """

    def get_bodies(self) -> ValuesView[BodyDescription]:
        """
        Retrieve the collection of body parts.
        """

    def get_body(self, name: str) -> BodyDescription | None:
        """
        Retrieve the body part description for the given name.
        """

    def get_children_for(self, body: BodyDescription | str) -> Generator[BodyDescription]:
        """
        Retrieve the collection of child body parts for the given body part.
        """

    def get_joints(self) -> ValuesView[JointDescription]:
        """
        Retrieve the collection of joints.
        """

    def get_joint(self, name: str) -> JointDescription | None:
        """
        Retrieve the collection of joints.
        """

    def get_joint_for(self, body: BodyDescription | str) -> JointDescription | None:
        """
        Retrieve the joint description for the given body part description.
        """

    def get_sensors(self) -> ValuesView[SensorDescription]:
        """
        Retrieve the collection of sensors.
        """

    def get_actuators(self) -> ValuesView[ActuatorDescription]:
        """
        Retrieve the collection of actuators.
        """


@dataclass(frozen=True)
class SensorDescription:
    """
    Base class for sensor descriptions.
    """

    name: str
    """
    The name of the sensor.
    """

    frame_id: str
    """
    The frame-id (the name of the body) the sensor is attached to.
    """

    perceptor_name: str
    """
    The name of the perceptor.
    """

    sensor_type: str
    """
    The sensor type information.
    """


@dataclass(frozen=True)
class GyroDescription(SensorDescription):
    """
    Default gyro sensor description.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str):
        super().__init__(name, frame_id, perceptor_name, SensorType.GYRO.value)


@dataclass(frozen=True)
class AccelerometerDescription(SensorDescription):
    """
    Default accelerometer sensor description.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str):
        super().__init__(name, frame_id, perceptor_name, SensorType.ACCELEROMETER.value)


@dataclass(frozen=True)
class IMUDescription(SensorDescription):
    """
    Default IMU sensor description.
    """

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str):
        super().__init__(name, frame_id, perceptor_name, SensorType.IMU.value)


@dataclass(frozen=True)
class CameraDescription(SensorDescription):
    """
    Default camera sensor description.
    """

    horizontal_fov: float
    vertical_fov: float

    def __init__(self,
                 name: str,
                 frame_id: str,
                 perceptor_name: str,
                 horizontal_fov: float,
                 vertical_fov: float):
        super().__init__(name, frame_id, perceptor_name, SensorType.CAMERA.value)

        object.__setattr__(self, 'horizontal_fov', horizontal_fov)
        object.__setattr__(self, 'vertical_fov', vertical_fov)


@dataclass(frozen=True)
class ActuatorDescription:
    """
    Base class for actuator descriptions.
    """

    name: str
    """
    The name of the actuator.
    """

    effector_name: str
    """
    The name of the effector associated with the actuator.
    """

    actuator_type: str
    """
    The actuator type information.
    """


@dataclass(frozen=True)
class MotorDescription:
    """
    Default motor actuator description.
    """

    effector_name: str
    """
    The name of the effector associated with the actuator.
    """

    max_speed: float
    """
    The maximum possible speed of the motor.
    """

    max_effort: float = 0.0
    """
    The maximum possible force / torque of the motor.
    """


@dataclass(frozen=True)
class JointDescription:
    """
    Description of a joint connection between two body parts.
    """

    name: str
    """
    The name of the joint.
    """

    parent: str
    """
    The parent body of the joint.
    """

    child: str
    """
    The child body of the joint.
    """

    joint_type: str
    """
    The joint type information.
    """

    anchor: Vector3D
    """
    The joint anchor.
    """


@dataclass(frozen=True)
class FixedJointDescription(JointDescription):
    """
    Description of a fixed joint connection between two body parts.
    """

    orientation: Rotation3D
    """
    The fixed orientation of the joint.
    """

    def __init__(self,
                 name: str,
                 parent: str,
                 child: str,
                 anchor: Vector3D,
                 orientation: Rotation3D | None = None) -> None:
        super().__init__(name, parent, child, JointType.FIXED.value, anchor)

        object.__setattr__(self, 'orientation', Rotation3D() if orientation is None else orientation)


@dataclass(frozen=True)
class HingeJointDescription(JointDescription):
    """
    Description of a 1DOF hinge joint connection between two body parts.
    """

    perceptor_name: str
    """
    The perceptor name of the corresponding joint sensor (if existing).
    """

    axis: Vector3D
    """
    The axis of this hinge joint.
    """

    limits: Vector2D
    """
    The axis limits of this hinge joint.
    """

    motor: MotorDescription | None
    """
    Description of the motor driving this joint.
    """

    def __init__(self,
                 name: str,
                 parent: str,
                 child: str,
                 perceptor_name: str,
                 anchor: Vector3D,
                 axis: Vector3D,
                 limits: Vector2D,
                 motor: MotorDescription | None = None) -> None:
        super().__init__(name, parent, child, JointType.HINGE.value, anchor)

        object.__setattr__(self, 'perceptor_name', perceptor_name)
        object.__setattr__(self, 'axis', axis)
        object.__setattr__(self, 'limits', limits)
        object.__setattr__(self, 'motor', motor)


@dataclass(frozen=True)
class FreeJointDescription(JointDescription):
    """
    Description of a 6DOF free joint connection between two body parts.
    """

    perceptor_name: str
    """
    The perceptor name of the corresponding joint sensor (if existing).
    """

    def __init__(self,
                 name: str,
                 parent: str,
                 child: str,
                 perceptor_name: str,
                 anchor: Vector3D):
        super().__init__(name, parent, child, JointType.FREE.value, anchor)

        object.__setattr__(self, 'perceptor_name', perceptor_name)


@dataclass(frozen=True)
class BodyDescription:
    """
    Description of a body part of the robot.
    """

    name: str
    """
    The name of the body.
    """

    translation: Vector3D
    """
    The translation of the body.
    """


class RobotDescription:
    """
    Representation of a robot description.
    """

    def __init__(self, name: str) -> None:

        self._name: str = name
        self._bodies: dict[str, BodyDescription] = {}
        self._joints: dict[str, JointDescription] = {}
        self._sensors: dict[str, SensorDescription] = {}
        self._actuators: dict[str, ActuatorDescription] = {}

    def get_name(self) -> str:
        """
        Retrieve the name of the robot model.
        """

        return self._name

    def get_root_body(self) -> BodyDescription:
        """
        Retrieve the root body part.
        """

        no_parent_bodies = [body for body in self._bodies.values() if self.get_joint_for(body) is None]
        n_bodies = len(no_parent_bodies)

        if n_bodies == 1:
            return no_parent_bodies[0]
        if n_bodies > 1:
            msg = 'No unique root body part: Found multiple non-parent body parts!'
            raise ValueError(msg)

        msg = 'No root body part!'
        raise ValueError(msg)

    def get_bodies(self) -> ValuesView[BodyDescription]:
        """
        Retrieve the collection of body parts.
        """

        return self._bodies.values()

    def get_body(self, name: str) -> BodyDescription | None:
        """
        Retrieve the body part description for the given name.
        """

        return self._bodies.get(name, None)

    def get_children_for(self, body: BodyDescription | str) -> Generator[BodyDescription]:
        """
        Retrieve the collection of child body parts for the given body part.
        """

        if isinstance(body, BodyDescription):
            body = body.name

        return (self._bodies[joint.child] for joint in self._joints.values() if joint.parent == body)

    def get_joints(self) -> ValuesView[JointDescription]:
        """
        Retrieve the collection of joints.
        """

        return self._joints.values()

    def get_joint(self, name: str) -> JointDescription | None:
        """
        Retrieve the collection of joints.
        """

        return self._joints.get(name, None)

    def get_joint_for(self, body: BodyDescription | str) -> JointDescription | None:
        """
        Retrieve the joint description for the given body part description.
        """

        if isinstance(body, BodyDescription):
            body = body.name

        joints = [joint for joint in self._joints.values() if joint.child == body]
        n_joints = len(joints)

        if n_joints == 1:
            return joints[0]
        if n_joints > 1:
            msg = f'The body "{body}" is apparently connected by multiple joints to its parent body!'
            raise ValueError(msg)

        return None

    def get_sensors(self) -> ValuesView[SensorDescription]:
        """
        Retrieve the collection of sensors.
        """

        return self._sensors.values()

    def get_actuators(self) -> ValuesView[ActuatorDescription]:
        """
        Retrieve the collection of actuators.
        """

        return self._actuators.values()

    def _add_body(self, desc: BodyDescription, *, override: bool = False) -> None:
        """
        Add the given body description to the dictionary of bodies.
        """

        if not override and desc.name in self._bodies:
            msg = f'A body with the name "{desc.name}" already exists!'
            raise ValueError(msg)

        self._bodies[desc.name] = desc

    def _add_joint(self, desc: JointDescription, *, override: bool = False) -> None:
        """
        Add the given joint description to the dictionary of joints.
        """

        if not override and desc.name in self._joints:
            msg = f'A joint with the name "{desc.name}" already exists!'
            raise ValueError(msg)

        self._joints[desc.name] = desc

    def _add_sensor(self, desc: SensorDescription, *, override: bool = False) -> None:
        """
        Add the given sensor description to the dictionary of sensors.
        """

        if not override and desc.name in self._sensors:
            msg = f'A sensor with the name "{desc.name}" already exists!'
            raise ValueError(msg)

        self._sensors[desc.name] = desc

    def _add_actuator(self, desc: ActuatorDescription, *, override: bool = False) -> None:
        """
        Add the given actuator description to the dictionary of actuators.
        """

        if not override and desc.name in self._actuators:
            msg = f'An actuator with the name "{desc.name}" already exists!'
            raise ValueError(msg)

        self._actuators[desc.name] = desc
