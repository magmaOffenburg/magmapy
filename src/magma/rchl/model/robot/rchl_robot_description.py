from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from magma.agent.model.robot.robot_description import ActuatorDescription, SensorDescription


class RCHLSensorType(Enum):
    """Specific sensor types used in RoboCup Soccer Humanoid league."""

    TEAM_COM = 'team_com'
    """A sensor, receiving team communication information."""


class RCHLActuatorType(Enum):
    """Specific actuator types used in RoboCup Soccer Humanoid league."""

    TEAM_COM = 'team_com'
    """A team communication actuator for sending messages to teammates."""


@dataclass(frozen=True)
class RCHLHearDescription(SensorDescription):
    """Soccer Humanoid team communication sensor description."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str):
        super().__init__(name, frame_id, perceptor_name, RCHLSensorType.TEAM_COM.value)


@dataclass(frozen=True)
class RCHLSayDescription(ActuatorDescription):
    """Soccer Humanoid team communication actuator description."""

    def __init__(self, name: str, effector_name: str):
        super().__init__(name, effector_name, RCHLActuatorType.TEAM_COM.value)
