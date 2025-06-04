from __future__ import annotations

from typing import TYPE_CHECKING

from magma.agent.model.robot.robot_model import BodyPart, RobotModel
from magma.rcss.model.robot.rcss_actuators import CreateActuator, InitActuator, PassModeActuator, Scotty, SyncActuator
from magma.rcss.model.robot.rcss_robot_description import RCSSActuatorType, RCSSSensorType
from magma.rcss.model.robot.rcss_sensors import ForceResistance
from magma.rcss.model.robot.spark_robot_description import InitDescription, SceneDescription, SyncDescription

if TYPE_CHECKING:
    from magma.agent.model.robot.actuators import Actuator
    from magma.agent.model.robot.robot_description import ActuatorDescription, SensorDescription
    from magma.agent.model.robot.sensors import Sensor


class RCSSRobotModel(RobotModel):
    """
    Robot model implementation for RoboCup Soccer Simulation.
    """

    def __init__(self, sensors: list[Sensor], actuators: list[Actuator], root_body: BodyPart) -> None:
        """
        Construct a new RoboCup Soccer Simulation robot model.
        """

        super().__init__(sensors, actuators, root_body)

    @classmethod
    def _create_sensor(cls, desc: SensorDescription) -> Sensor | None:
        if desc.sensor_type == RCSSSensorType.FORCE_RESISTANCE.value:
            return ForceResistance(desc.name, desc.frame_id, desc.perceptor_name)

        # forward call to parent class
        return super()._create_sensor(desc)

    @classmethod
    def _create_actuator(cls, desc: ActuatorDescription) -> Actuator | None:
        if isinstance(desc, SceneDescription):
            return CreateActuator(desc.name, desc.effector_name, desc.scene, desc.model_type)

        if isinstance(desc, InitDescription):
            return InitActuator(desc.name, desc.effector_name, desc.model_name)

        if isinstance(desc, SyncDescription):
            return SyncActuator(desc.name, desc.effector_name, auto_active=desc.auto_sync)

        if desc.actuator_type == RCSSActuatorType.BEAM.value:
            return Scotty(desc.name, desc.effector_name)

        if desc.actuator_type == RCSSActuatorType.PASS_MODE.value:
            return PassModeActuator(desc.name, desc.effector_name)

        # forward call to parent class
        return super()._create_actuator(desc)
