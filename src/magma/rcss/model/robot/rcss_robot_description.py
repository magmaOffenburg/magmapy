from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from magma.agent.model.robot.robot_description import ActuatorDescription, SensorDescription


class RCSSSensorType(Enum):
    """Specific sensor types used in RoboCup Soccer Simulation."""

    FORCE_RESISTANCE = 'force_resistance'
    """A force sensor, receiving force information."""

    VISION = 'soccer_vision'
    """A virtual vision pipeline sensor, receiving various state information about visible objects, lines and players in the environment."""


class RCSSActuatorType(Enum):
    """Specific actuator types used in RoboCup Soccer Simulation."""

    SCENE = 'scene'
    """A scene actuator for spawning a robot."""

    INIT = 'init'
    """A init actuator for initializing a robot."""

    SYNC = 'sync'
    """A synchronize actuator."""

    BEAM = 'beam'
    """A beam actuator."""

    PASS_MODE = 'pass_mode'  # noqa: S105 - prevent ruff hardcoded-password-assignment warning
    """A pass mode actuator."""


@dataclass(frozen=True)
class ForceResistanceDescription(SensorDescription):
    """Default force resistance sensor description."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str):
        super().__init__(name, frame_id, perceptor_name, RCSSSensorType.FORCE_RESISTANCE.value)


@dataclass(frozen=True)
class RCSSVisionDescription(SensorDescription):
    """Soccer simulation vision pipeline sensor description."""

    horizontal_fov: float
    """The horizontal field of view angle."""

    vertical_fov: float
    """The vertical field of view angle."""

    def __init__(
        self,
        name: str,
        frame_id: str,
        perceptor_name: str,
        horizontal_fov: float,
        vertical_fov: float,
    ):
        super().__init__(name, frame_id, perceptor_name, RCSSSensorType.VISION.value)

        object.__setattr__(self, 'horizontal_fov', horizontal_fov)
        object.__setattr__(self, 'vertical_fov', vertical_fov)


@dataclass(frozen=True)
class SceneDescription(ActuatorDescription):
    """Default scene actuator description."""

    scene: str
    """The scene path."""

    model_type: int
    """The model type id."""

    def __init__(self, name: str, effector_name: str, scene: str, model_type: int):
        super().__init__(name, effector_name, RCSSActuatorType.SCENE.value)

        object.__setattr__(self, 'scene', scene)
        object.__setattr__(self, 'model_type', model_type)


@dataclass(frozen=True)
class InitDescription(ActuatorDescription):
    """Default init actuator description."""

    model_name: str
    """The name of the robot model."""

    def __init__(self, name: str, effector_name: str, model_name: str = ''):
        super().__init__(name, effector_name, RCSSActuatorType.INIT.value)

        object.__setattr__(self, 'model_name', model_name)


@dataclass(frozen=True)
class SyncDescription(ActuatorDescription):
    """Default synchronize actuator description."""

    auto_sync: bool
    """Flag for enabling auto sync."""

    def __init__(self, name: str, effector_name: str, *, auto_sync: bool = True):
        super().__init__(name, effector_name, RCSSActuatorType.SYNC.value)

        object.__setattr__(self, 'auto_sync', auto_sync)


@dataclass(frozen=True)
class BeamDescription(ActuatorDescription):
    """Default beam actuator description."""

    def __init__(self, name: str, effector_name: str):
        super().__init__(name, effector_name, RCSSActuatorType.BEAM.value)


@dataclass(frozen=True)
class PassModeDescription(ActuatorDescription):
    """Default pass mode actuator description."""

    def __init__(self, name: str, effector_name: str):
        super().__init__(name, effector_name, RCSSActuatorType.PASS_MODE.value)
