from __future__ import annotations

from typing import TYPE_CHECKING

from magma.agent.model.robot.robot_model import BodyPart, RobotModel
from magma.rchl.model.robot.rchl_actuators import RCHLTeamComActuator
from magma.rchl.model.robot.rchl_robot_description import RCHLActuatorType, RCHLSensorType
from magma.rchl.model.robot.rchl_sensors import RCHLTeamComSensor

if TYPE_CHECKING:
    from magma.agent.model.robot.actuators import Actuator
    from magma.agent.model.robot.robot_description import ActuatorDescription, SensorDescription
    from magma.agent.model.robot.sensors import Sensor


class RCHLRobotModel(RobotModel):
    """Robot model implementation for RoboCup Soccer Humanoid league."""

    def __init__(self, sensors: list[Sensor], actuators: list[Actuator], root_body: BodyPart) -> None:
        """Construct a new RoboCup Soccer Humanoid league robot model.

        Parameter
        ---------
        sensors : Iterable[Sensor]
            The collection of sensors of the robot model.

        actuators : Iterable[Actuator]
            The collection of actuators of the robot model.

        root_body : BodyPart
            The root body part of the robot body tree.
        """

        super().__init__(sensors, actuators, root_body)

    @classmethod
    def _create_sensor(cls, desc: SensorDescription) -> Sensor | None:
        if desc.sensor_type == RCHLSensorType.TEAM_COM.value:
            return RCHLTeamComSensor(desc.name, desc.frame_id, desc.perceptor_name)

        # forward call to parent class
        return super()._create_sensor(desc)

    @classmethod
    def _create_actuator(cls, desc: ActuatorDescription) -> Actuator | None:
        if desc.actuator_type == RCHLActuatorType.TEAM_COM.value:
            return RCHLTeamComActuator(desc.name, desc.effector_name)

        # forward call to parent class
        return super()._create_actuator(desc)
