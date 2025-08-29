from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from magma.agent.communication.action import Action
from magma.agent.model.robot.actuators import Actuator, Motor, OmniSpeedActuator
from magma.agent.model.robot.robot_description import (
    ActuatorDescription,
    ActuatorType,
    BodyDescription,
    CameraDescription,
    FixedJointDescription,
    FreeJointDescription,
    HingeJointDescription,
    JointDescription,
    PRobotDescription,
    SensorDescription,
    SensorType,
    VisionDescription,
)
from magma.agent.model.robot.robot_tree import ZERO_INERTIA, BodyPart, BodyVisual, FixedJoint, FreeJoint, HingeJoint, Joint, PBodyPart, RigidBodyInertia
from magma.agent.model.robot.sensors import (
    IMU,
    Accelerometer,
    Camera,
    FreeJointSensor,
    Gyroscope,
    HingeJointSensor,
    Loc2DSensor,
    Loc3DSensor,
    Sensor,
    VisionSensor,
)

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from magma.agent.communication.perception import Perception


ST = TypeVar('ST')
AT = TypeVar('AT')


class PRobotModel(Protocol):
    """Protocol for robot models."""

    def get_time(self) -> float:
        """Retrieve the time of the last update."""

    def get_sensor(self, name: str, s_type: type[ST]) -> ST | None:
        """Retrieve the sensor with the given name and type.

        Parameter
        ---------
        name : str
            The name of the sensor.

        s_type : type[ST]
            The expected sensor type.
        """

    def get_sensors(self, s_type: type[ST]) -> Generator[ST]:
        """Retrieve all sensors of the given type.

        Parameter
        ---------
        s_type : type[ST]
            The sensor type to filter.
        """

    def get_actuator(self, name: str, a_type: type[AT]) -> AT | None:
        """Retrieve the actuator with the given name and type.

        Parameter
        ---------
        name : str
            The name of the actuator.

        a_type : type[AT]
            The expected actuator type.
        """

    def get_actuators(self, a_type: type[AT]) -> Generator[AT]:
        """Retrieve all actuators of the given type.

        Parameter
        ---------
        a_type : type[AT]
            The actuator type to filter.
        """

    def get_tree(self) -> PBodyPart:
        """Retrieve the robot tree."""

    def get_body(self, name: str) -> PBodyPart | None:
        """Retrieve the robot tree."""


class PMutableRobotModel(PRobotModel, Protocol):
    """Protocol for mutable robot models."""

    def update(self, perception: Perception) -> None:
        """Update the sensor states of the robot model from the given perceptions.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """

    def generate_action(self) -> Action:
        """Generate a set of actions from all available actuators."""


class RobotModel:
    """Default robot model implementation."""

    def __init__(self, sensors: Iterable[Sensor], actuators: Iterable[Actuator], root_body: BodyPart) -> None:
        """Construct a new robot model.

        Parameter
        ---------
        sensors : Iterable[Sensor]
            The collection of sensors of the robot model.

        actuators : Iterable[Actuator]
            The collection of actuators of the robot model.

        root_body : BodyPart
            The root body part of the robot body tree.
        """

        self._time: float = 0.0
        """The current global time."""

        self._sensors: dict[str, Sensor] = {sensor.name: sensor for sensor in sensors}
        """The map of known sensors."""

        self._actuators: dict[str, Actuator] = {actuator.name: actuator for actuator in actuators}
        """The map of known actuators."""

        self._root_body: BodyPart = root_body
        """The root body part of the robot body tree."""

    def get_time(self) -> float:
        """Retrieve the time of the last update."""

        return self._time

    def get_sensor(self, name: str, s_type: type[ST]) -> ST | None:
        """Retrieve the sensor with the given name and type.

        Parameter
        ---------
        name : str
            The name of the sensor.

        s_type : type[ST]
            The expected sensor type.
        """

        sensor = self._sensors.get(name, None)
        return sensor if sensor is not None and isinstance(sensor, s_type) else None

    def get_sensors(self, s_type: type[ST]) -> Generator[ST]:
        """Retrieve all sensors of the given type.

        Parameter
        ---------
        s_type : type[ST]
            The sensor type to filter.
        """

        return (sensor for sensor in self._sensors.values() if isinstance(sensor, s_type))

    def get_actuator(self, name: str, a_type: type[AT]) -> AT | None:
        """Retrieve the actuator with the given name and type.

        Parameter
        ---------
        name : str
            The name of the actuator.

        a_type : type[AT]
            The expected actuator type.
        """

        actuator = self._actuators.get(name, None)
        return actuator if actuator is not None and isinstance(actuator, a_type) else None

    def get_actuators(self, a_type: type[AT]) -> Generator[AT]:
        """Retrieve all actuators of the given type.

        Parameter
        ---------
        a_type : type[AT]
            The actuator type to filter.
        """

        return (actuator for actuator in self._actuators.values() if isinstance(actuator, a_type))

    def get_tree(self) -> BodyPart:
        """Retrieve the robot tree."""

        return self._root_body

    def get_body(self, name: str) -> PBodyPart | None:
        """Retrieve the robot tree."""

        return self._root_body.get_body(name)

    def update(self, perception: Perception) -> None:
        """Update the state of the robot model from the given perceptions.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information to process.
        """

        self._time = perception.get_time()

        # update sensors
        for sensor in self._sensors.values():
            sensor.update(perception)

    def generate_action(self) -> Action:
        """Generate a set of actions from all available actuators."""

        action = Action()

        # collect actuator actions
        for actuator in self._actuators.values():
            actuator.commit(action)

        return action

    @classmethod
    def from_description(cls, desc: PRobotDescription) -> RobotModel:
        """Construct a new robot model from the given description.

        Parameter
        ---------
        desc : PRobotDescription
            The robot description from which to create a new robot model instance.
        """

        sensors: list[Sensor] = []
        actuators: list[Actuator] = []

        # create body tree
        root_body = cls._create_body(desc.get_root_body(), desc, sensors, actuators)

        # create sensors
        for sensor_desc in desc.get_sensors():
            sensor = cls._create_sensor(sensor_desc)
            if sensor is not None:
                sensors.append(sensor)

        # create actuators
        for actuator_desc in desc.get_actuators():
            actuator = cls._create_actuator(actuator_desc)
            if actuator is not None:
                actuators.append(actuator)

        return RobotModel(sensors, actuators, root_body)

    @classmethod
    def _create_body(cls, body: BodyDescription, robot: PRobotDescription, sensors: list[Sensor], actuators: list[Actuator]) -> BodyPart:
        """Create a body part representation for the given description.

        Parameter
        ---------
        body : BodyDescription
            The description of the body to create.

        robot : PRobotDescription
            The robot description.

        sensors : list[Sensor]
            The central sensor list to which to add new sensors attached to the body.

        actuators : list[Actuator]
            The central actuators list to which to add new actuators attached to the body.
        """

        # create child body parts
        children = tuple(cls._create_body(child_desc, robot, sensors, actuators) for child_desc in robot.get_children_for(body))

        # create rigid body inertia
        inertia = ZERO_INERTIA if body.inertia is None else RigidBodyInertia(body.inertia.origin, body.inertia.mass, body.inertia.inertia)

        # create joint
        joint = cls._create_joint(robot.get_joint_for(body), sensors, actuators)

        # create body appearance
        appearance = None if body.visual is None else BodyVisual(body.visual.origin, body.visual.geometry)

        # create body part
        return BodyPart(body.name, children, inertia, joint, appearance)

    @classmethod
    def _create_joint(cls, desc: JointDescription | None, sensors: list[Sensor], actuators: list[Actuator]) -> Joint | None:
        """Create a joint representation for the given description.

        Parameter
        ---------
        body : JointDescription | None
            The description of the joint to create (if existing).

        sensors : list[Sensor]
            The central sensor list to which to add new sensors attached to the body.

        actuators : list[Actuator]
            The central actuators list to which to add new actuators attached to the body.
        """

        joint: Joint | None = None

        if desc is None:
            # no description -> no joint
            joint = None

        elif isinstance(desc, FixedJointDescription):
            joint = FixedJoint(desc.name, desc.anchor, desc.orientation)

        elif isinstance(desc, HingeJointDescription):
            joint = HingeJoint(desc.name, desc.anchor, desc.axis, desc.limits)
            sensors.append(HingeJointSensor(desc.name, desc.child, desc.perceptor_name, joint))
            if desc.motor is not None:
                actuators.append(Motor(desc.name, desc.motor.effector_name, desc.motor.max_speed, desc.motor.max_effort, joint))

        elif isinstance(desc, FreeJointDescription):
            joint = FreeJoint(desc.name, desc.anchor)
            sensors.append(FreeJointSensor(desc.name, desc.child, desc.perceptor_name, joint))

        else:
            msg = f'Unknown joint description for "{desc.name}" of type "{desc.joint_type}"!'
            raise ValueError(msg)

        return joint

    @classmethod
    def _create_sensor(cls, desc: SensorDescription) -> Sensor | None:
        """Create a sensor representation for the given description.

        Parameter
        ---------
        desc : SensorDescription
            The description for which to create a sensor instance.
        """

        if desc.sensor_type == SensorType.GYRO.value:
            return Gyroscope(desc.name, desc.frame_id, desc.perceptor_name)

        if desc.sensor_type == SensorType.ACCELEROMETER.value:
            return Accelerometer(desc.name, desc.frame_id, desc.perceptor_name)

        if desc.sensor_type == SensorType.IMU.value:
            return IMU(desc.name, desc.frame_id, desc.perceptor_name)

        if desc.sensor_type == SensorType.CAMERA.value and isinstance(desc, CameraDescription):
            return Camera(desc.name, desc.frame_id, desc.perceptor_name, desc.horizontal_fov, desc.vertical_fov)

        if desc.sensor_type == SensorType.VISION.value and isinstance(desc, VisionDescription):
            return VisionSensor(desc.name, desc.frame_id, desc.perceptor_name, desc.horizontal_fov, desc.vertical_fov)

        if desc.sensor_type == SensorType.LOC2D.value:
            return Loc2DSensor(desc.name, desc.frame_id, desc.perceptor_name)

        if desc.sensor_type == SensorType.LOC3D.value:
            return Loc3DSensor(desc.name, desc.frame_id, desc.perceptor_name)

        print(f'WARNING: Unknown sensor description for "{desc.name}" of type "{desc.sensor_type}"!')  # noqa: T201

        return None

    @classmethod
    def _create_actuator(cls, desc: ActuatorDescription) -> Actuator | None:
        """Create an actuator representation for the given description.

        Parameter
        ---------
        desc : ActuatorDescription
            The description for which to create a actuator instance.
        """

        if desc.actuator_type == ActuatorType.OMNI_SPEED.value:
            return OmniSpeedActuator(desc.name, desc.effector_name)

        print(f'WARNING: Unknown actuator description for "{desc.name}" of type "{desc.actuator_type}"!')  # noqa: T201

        return None
