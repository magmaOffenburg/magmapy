from __future__ import annotations

from typing import TYPE_CHECKING

from magmapy.agent.model.robot.robot_model import BodyPart, RobotModel
from magmapy.rcss.model.robot.rcss_actuators import InitActuator, Scotty, SyncActuator
from magmapy.rcss.model.robot.rcss_robot_description import InitDescription, RCSSActuatorType, RCSSSensorType, RCSSVisionDescription, SyncDescription
from magmapy.rcss.model.robot.rcss_sensors import RCSSVisionSensor

if TYPE_CHECKING:
    from magmapy.agent.model.robot.actuators import Actuator
    from magmapy.agent.model.robot.robot_description import ActuatorDescription, SensorDescription
    from magmapy.agent.model.robot.sensors import Sensor


class RCSSRobotModel(RobotModel):
    """Robot model implementation for RoboCup Soccer Simulation (MuJoCo)."""

    def __init__(self, sensors: list[Sensor], actuators: list[Actuator], root_body: BodyPart) -> None:
        """Construct a new RoboCup Soccer Simulation robot model.

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
        if desc.sensor_type == RCSSSensorType.VISION.value and isinstance(desc, RCSSVisionDescription):
            return RCSSVisionSensor(desc.name, desc.frame_id, desc.perceptor_name, desc.horizontal_fov, desc.vertical_fov)

        # forward call to parent class
        return super()._create_sensor(desc)

    @classmethod
    def _create_actuator(cls, desc: ActuatorDescription) -> Actuator | None:
        if desc.actuator_type == RCSSActuatorType.INIT.value and isinstance(desc, InitDescription):
            return InitActuator(desc.name, desc.effector_name, desc.model_name)

        if desc.actuator_type == RCSSActuatorType.SYNC.value and isinstance(desc, SyncDescription):
            return SyncActuator(desc.name, desc.effector_name, auto_active=desc.auto_sync)

        if desc.actuator_type == RCSSActuatorType.BEAM.value:
            return Scotty(desc.name, desc.effector_name)

        # forward call to parent class
        return super()._create_actuator(desc)
