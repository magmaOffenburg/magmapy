from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from magma.agent.communication.action import Action
from magma.agent.model.base import PMutableModel
from magma.agent.model.robot.actuators import Actuator, Motor
from magma.agent.model.robot.robot_description import (
    ActuatorDescription,
    BodyDescription,
    FixedJointDescription,
    FreeJointDescription,
    HingeJointDescription,
    JointDescription,
    PRobotDescription,
    SensorDescription,
    SensorType,
)
from magma.agent.model.robot.robot_tree import BodyPart, FixedJoint, FreeJoint, HingeJoint, Joint, PBodyPart
from magma.agent.model.robot.sensors import (
    IMU,
    Accelerometer,
    FreeJointSensor,
    Gyroskope,
    HingeJointSensor,
    Sensor,
)

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from magma.agent.communication.perception import Perception


ST = TypeVar("ST")
AT = TypeVar("AT")

class PRobotModel(Protocol):
    """
    Protocol for robot models.
    """

    def get_time(self) -> float:
        """
        Retrieve the time of the last update.
        """

    def get_sensor(self, name: str, s_type: type[ST]) -> ST | None:
        """
        Retrieve the sensor with the given name and type.
        """

    def get_sensors(self, s_type: type[ST]) -> Generator[ST]:
        """
        Retrieve all sensors of the given type.
        """

    def get_actuator(self, name: str, a_type: type[AT]) -> AT | None:
        """
        Retrieve the actuator with the given name and type.
        """

    def get_actuators(self, a_type: type[AT]) -> Generator[AT]:
        """
        Retrieve all actuators of the given type.
        """

    def get_tree(self) -> PBodyPart:
        """
        Retrieve the robot tree.
        """


class PMutableRobotModel(PRobotModel, PMutableModel, Protocol):
    """
    Protocol for mutable robot models.
    """

    def generate_action(self) -> Action:
        """
        Generate a set of actions from all available actuators.
        """


class RobotModel:
    """
    Default robot model implementation.
    """

    def __init__(self,
                 sensors: Iterable[Sensor],
                 actuators: Iterable[Actuator],
                 root_body: BodyPart) -> None:
        """
        Construct a new robot model.
        """

        self._time: float = 0.0
        self._sensors: dict[str, Sensor] = {sensor.get_name(): sensor for sensor in sensors}
        self._actuators: dict[str, Actuator] = {actuator.get_name(): actuator for actuator in actuators}
        self._root_body: BodyPart = root_body

    def get_time(self) -> float:
        """
        Retrieve the time of the last update.
        """

        return self._time

    def get_sensor(self, name: str, s_type: type[ST]) -> ST | None:
        """
        Retrieve the sensor with the given name and type.
        """

        sensor = self._sensors.get(name, None)
        return sensor if sensor is not None and isinstance(sensor, s_type) else None

    def get_sensors(self, s_type: type[ST]) -> Generator[ST]:
        """
        Retrieve all sensors of the given type.
        """

        return (sensor for sensor in self._sensors.values() if isinstance(sensor, s_type))

    def get_actuator(self, name: str, a_type: type[AT]) -> AT | None:
        """
        Retrieve the actuator with the given name and type.
        """

        actuator = self._actuators.get(name, None)
        return actuator if actuator is not None and isinstance(actuator, a_type) else None

    def get_actuators(self, a_type: type[AT]) -> Generator[AT]:
        """
        Retrieve all actuators of the given type.
        """

        return (actuator for actuator in self._actuators.values() if isinstance(actuator, a_type))

    def get_tree(self) -> BodyPart:
        """
        Retrieve the robot tree.
        """

        return self._root_body

    def update(self, perception: Perception) -> None:
        """
        Update the state of the robot model from the given perceptions.
        """

        self._time = perception.get_time()

        # update sensors
        for sensor in self._sensors.values():
            sensor.update(perception)

    def generate_action(self) -> Action:
        """
        Generate a set of actions from all available actuators.
        """

        action = Action()

        # collect actuator actions
        for actuator in self._actuators.values():
            actuator.commit(action)

        return action

    @classmethod
    def from_description(cls, desc: PRobotDescription) -> RobotModel:
        """
        Construct a new robot model from the given description.
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
        """
        Create a body part representation for the given description.
        """

        # create child body parts
        children = tuple(cls._create_body(child_desc, robot, sensors, actuators) for child_desc in robot.get_children_for(body))

        # create joint
        joint = cls._create_joint(robot.get_joint_for(body), sensors, actuators)

        # create body part
        return BodyPart(body.name, children, body.translation, joint)

    @classmethod
    def _create_joint(cls, desc: JointDescription | None, sensors: list[Sensor], actuators: list[Actuator]) -> Joint | None:
        """
        Create a joint representation for the given description.
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
        """
        Create a sensor representation for the given description.
        """

        if desc.sensor_type == SensorType.GYRO.value:
            return Gyroskope(desc.name, desc.frame_id, desc.perceptor_name)

        if desc.sensor_type == SensorType.ACCELEROMETER.value:
            return Accelerometer(desc.name, desc.frame_id, desc.perceptor_name)

        if desc.sensor_type == SensorType.IMU.value:
            return IMU(desc.name, desc.frame_id, desc.perceptor_name)

        print(f'WARNING: Unknown sensor description for "{desc.name}" of type "{desc.sensor_type}"!')  # noqa: T201

        return None

    @classmethod
    def _create_actuator(cls, desc: ActuatorDescription) -> Actuator | None:
        """
        Create an actuator representation for the given description.
        """

        print(f'WARNING: Unknown actuator description for "{desc.name}" of type "{desc.actuator_type}"!')  # noqa: T201

        return None
