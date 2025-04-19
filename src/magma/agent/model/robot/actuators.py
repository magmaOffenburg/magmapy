from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magma.agent.communication.action import Action, MotorEffector, OmniSpeedEffector

if TYPE_CHECKING:
    from magma.agent.model.robot.robot_tree import HingeJoint
    from magma.common.math.geometry.vector import Vector3D


@runtime_checkable
class PActuator(Protocol):
    """
    Protocol for actuators of a robot model.
    """

    @property
    def name(self) -> str:
        """
        The name of the actuator.
        """


@runtime_checkable
class PMotor(PActuator, Protocol):
    """
    Protocol for motor actuators.
    """

    def set(self, target_pos: float, target_vel: float, kp: float, kd: float) -> None:
        """
        Set the motor action.
        """

    @property
    def max_velocity(self) -> float:
        """
        The maximum motor velocity.
        """

    @property
    def max_effort(self) -> float:
        """
        The maximum motor effort (force / torque).
        """

    def get_target_position(self) -> float:
        """
        Retrieve the target position.
        """

    def get_target_velocity(self) -> float:
        """
        Retrieve the target velocity.
        """

    def get_target_kp(self) -> float:
        """
        Retrieve the target kp.
        """

    def get_target_kd(self) -> float:
        """
        Retrieve the target kd.
        """

    def get_prev_target_position(self) -> float:
        """
        Retrieve the previously performed target position.
        """

    def get_prev_target_velocity(self) -> float:
        """
        Retrieve the previously performed target velocity.
        """

    def get_prev_target_kp(self) -> float:
        """
        Retrieve the previously performed target kp.
        """

    def get_prev_target_kd(self) -> float:
        """
        Retrieve the previously performed target kd.
        """


@runtime_checkable
class POmniSpeedActuator(PActuator, Protocol):
    """
    Protocol for omni-directional speed actuators.
    """

    def set(self, desired_speed: Vector3D) -> None:
        """
        Set the omni-directional speed action.
        """

    def get_desired_speed(self) -> Vector3D | None:
        """
        Retrieve the desired speed.
        """


class Actuator(ABC):
    """
    Base class for all actuators of a robot model.
    """

    def __init__(self, name: str, effector_name: str):
        """
        Construct a new actuator.
        """

        super().__init__()

        self.name: Final[str] = name
        self.effector_name: Final[str] = effector_name

    @abstractmethod
    def commit(self, action: Action) -> None:
        """
        Commit an action command for this actuator to the action map.
        """


class Motor(Actuator):
    """
    Default implementation of a motor controlling a joint.
    """

    def __init__(
        self,
        name: str,
        effector_name: str,
        max_speed: float,
        max_effort: float,
        joint: HingeJoint,
    ):
        """
        Construct a new motor.
        """

        super().__init__(name, effector_name)

        self.max_velocity: Final[float] = max_speed
        self.max_effort: Final[float] = max_effort
        self.joint: Final[HingeJoint] = joint

        self._target_position: float = 0.0
        self._target_velocity: float = 0.0
        self._target_kp: float = 0.0
        self._target_kd: float = 0.0

        self._previous_target_position: float = 0.0
        self._previous_target_velocity: float = 0.0
        self._previous_target_kp: float = 0.0
        self._previous_target_kd: float = 0.0

    def set(self, pos: float, vel: float, kp: float, kd: float) -> None:
        """
        Set the motor target action.
        """

        self._target_position = pos
        self._target_velocity = vel
        self._target_kp = kp
        self._target_kd = kd

    def get_target_position(self) -> float:
        """
        Retrieve the target position.
        """

        return self._target_position

    def get_target_velocity(self) -> float:
        """
        Retrieve the target velocity.
        """

        return self._target_velocity

    def get_target_kp(self) -> float:
        """
        Retrieve the target kp.
        """

        return self._target_kp

    def get_target_kd(self) -> float:
        """
        Retrieve the target kd.
        """

        return self._target_kd

    def get_prev_target_position(self) -> float:
        """
        Retrieve the previously performed target position.
        """

        return self._previous_target_position

    def get_prev_target_velocity(self) -> float:
        """
        Retrieve the previously performed target velocity.
        """

        return self._previous_target_velocity

    def get_prev_target_kp(self) -> float:
        """
        Retrieve the previously performed target kp.
        """

        return self._previous_target_kp

    def get_prev_target_kd(self) -> float:
        """
        Retrieve the previously performed target kd.
        """

        return self._previous_target_kd

    def commit(self, action: Action) -> None:
        action.put(MotorEffector(self.effector_name, self._target_position, self._target_velocity, self._target_kp, self._target_kd))

        # set current target as previous targets
        self._previous_target_position = self._target_position
        self._previous_target_velocity = self._target_velocity
        self._previous_target_kp = self._target_kp
        self._previous_target_kd = self._target_kd


class OmniSpeedActuator(Actuator):
    """
    Default omni-directional speed actuator implementation.
    """

    def __init__(self, name: str, effector_name: str) -> None:
        """
        Create a new omni-directional speed actuator.
        """

        super().__init__(name, effector_name)

        self._desired_speed: Vector3D | None = None

    def set(self, desired_speed: Vector3D) -> None:
        """
        Set the omni-directional speed action.
        """

        self._desired_speed = desired_speed

    def get_desired_speed(self) -> Vector3D | None:
        """
        Retrieve the desired speed.
        """

        return self._desired_speed

    def commit(self, action: Action) -> None:
        if self._desired_speed is not None:
            action.put(OmniSpeedEffector(self.effector_name, self._desired_speed))

        # reset actuator
        self._desired_speed = None
