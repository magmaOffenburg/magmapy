from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magmapy.agent.communication.action import Action, MotorEffector, OmniSpeedEffector

if TYPE_CHECKING:
    from magmapy.agent.model.robot.robot_tree import HingeJoint
    from magmapy.common.math.geometry.vector import Vector3D


@runtime_checkable
class PActuator(Protocol):
    """Protocol for actuators of a robot model."""

    @property
    def name(self) -> str:
        """The name of the actuator."""


@runtime_checkable
class PMotor(PActuator, Protocol):
    """Protocol for motor actuators."""

    def set(self, target_pos: float, target_vel: float, kp: float, kd: float) -> None:
        """Set the motor action."""

    @property
    def max_velocity(self) -> float:
        """The maximum motor velocity."""

    @property
    def max_effort(self) -> float:
        """The maximum motor effort (force / torque)."""

    def get_target_position(self) -> float:
        """Retrieve the target position."""

    def get_target_velocity(self) -> float:
        """Retrieve the target velocity."""

    def get_target_kp(self) -> float:
        """Retrieve the target kp."""

    def get_target_kd(self) -> float:
        """Retrieve the target kd."""

    def get_target_tau(self) -> float:
        """Retrieve the target torque."""

    def get_prev_target_position(self) -> float:
        """Retrieve the previously performed target position."""

    def get_prev_target_velocity(self) -> float:
        """Retrieve the previously performed target velocity."""

    def get_prev_target_kp(self) -> float:
        """Retrieve the previously performed target kp."""

    def get_prev_target_kd(self) -> float:
        """Retrieve the previously performed target kd."""

    def get_prev_target_tau(self) -> float:
        """Retrieve the previously performed target torque."""


@runtime_checkable
class POmniSpeedActuator(PActuator, Protocol):
    """Protocol for omni-directional speed actuators."""

    def set(self, desired_speed: Vector3D) -> None:
        """Set the omni-directional speed action."""

    def get_desired_speed(self) -> Vector3D | None:
        """Retrieve the desired speed."""


class Actuator(ABC):
    """Base class for all actuators of a robot model."""

    def __init__(self, name: str, effector_name: str):
        """Construct a new actuator.

        Parameter
        ---------
        name : str
            The name of the actuator.

        effector_name : str
            The name of the effector associated with this actuator.
        """

        super().__init__()

        self.name: Final[str] = name
        """The name of the actuator."""

        self.effector_name: Final[str] = effector_name
        """The name of the effector associated with this actuator."""

    @abstractmethod
    def commit(self, action: Action) -> None:
        """Commit an action command for this actuator to the action map.

        Parameter
        ---------
        action : Action
            The collection of actions to which to commit the actuator action.
        """


class Motor(Actuator):
    """Default implementation of a motor controlling a joint."""

    def __init__(
        self,
        name: str,
        effector_name: str,
        max_speed: float,
        max_effort: float,
        joint: HingeJoint,
    ):
        """Construct a new motor.

        Parameter
        ---------

        name : str
            The unique name of the motor.

        effector_name : str
            The name of the effector associated with this motor.

        max_speed : float
            The maximum velocity at which the motor can move / rotate.

        max_effort : float
            The maximum force / torque the motor can produce.

        joint : HingeJoint
            The joint the motor is driving.
        """

        super().__init__(name, effector_name)

        self.max_velocity: Final[float] = max_speed
        """The maximum velocity at which this motor can move / rotate."""

        self.max_effort: Final[float] = max_effort
        """The maximum force / torque this motor can produce."""

        self.joint: Final[HingeJoint] = joint
        """The joint this motor is driving."""

        self._target_position: float = 0.0
        """The motor target position."""

        self._target_velocity: float = 0.0
        """The motor target velocity."""

        self._target_kp: float = 0.0
        """Gain parameter for position controller."""

        self._target_kd: float = 0.0
        """Gain parameter for velocity controller."""

        self._target_tau: float = 0.0
        """The motor target force / torque."""

        self._previous_target_position: float = 0.0
        """The previous motor target position."""

        self._previous_target_velocity: float = 0.0
        """The previous motor target velocity."""

        self._previous_target_kp: float = 0.0
        """The previous gain parameter for position controller."""

        self._previous_target_kd: float = 0.0
        """The previous gain parameter for velocity controller."""

        self._previous_target_tau: float = 0.0
        """The previous motor target force / torque."""

    def set(self, pos: float, vel: float, kp: float, kd: float, tau: float) -> None:
        """Set the motor target action.

        Parameter
        ---------
        pos : float
            The motor target position.

        vel : float
            The motor target velocity.

        kp : float
            Gain value for position controller.

        kd : float
            Gain value for velocity controller.

        tau : float
            Target motor force / torque.
        """

        self._target_position = pos
        self._target_velocity = vel
        self._target_kp = kp
        self._target_kd = kd
        self._target_tau = tau

    def get_target_position(self) -> float:
        """Retrieve the target position."""

        return self._target_position

    def get_target_velocity(self) -> float:
        """Retrieve the target velocity."""

        return self._target_velocity

    def get_target_kp(self) -> float:
        """Retrieve the target kp."""

        return self._target_kp

    def get_target_kd(self) -> float:
        """Retrieve the target kd."""

        return self._target_kd

    def get_target_tau(self) -> float:
        """Retrieve the target torque."""

        return self._target_tau

    def get_prev_target_position(self) -> float:
        """Retrieve the previously performed target position."""

        return self._previous_target_position

    def get_prev_target_velocity(self) -> float:
        """Retrieve the previously performed target velocity."""

        return self._previous_target_velocity

    def get_prev_target_kp(self) -> float:
        """Retrieve the previously performed target kp."""

        return self._previous_target_kp

    def get_prev_target_kd(self) -> float:
        """Retrieve the previously performed target kd."""

        return self._previous_target_kd

    def get_prev_target_tau(self) -> float:
        """Retrieve the previously performed target torque."""

        return self._previous_target_tau

    def commit(self, action: Action) -> None:
        action.put(MotorEffector(self.effector_name, self._target_position, self._target_velocity, self._target_kp, self._target_kd, self._target_tau))

        # set current target as previous targets
        self._previous_target_position = self._target_position
        self._previous_target_velocity = self._target_velocity
        self._previous_target_kp = self._target_kp
        self._previous_target_kd = self._target_kd
        self._previous_target_tau = self._target_tau


class OmniSpeedActuator(Actuator):
    """Default omni-directional speed actuator implementation."""

    def __init__(self, name: str, effector_name: str) -> None:
        """Create a new omni-directional speed actuator.

        Parameter
        ---------
        name : str
            The name of the actuator.

        effector_name : str
            The name of the effector associated with this actuator.
        """

        super().__init__(name, effector_name)

        self._desired_speed: Vector3D | None = None
        """The desired movement speed."""

    def set(self, desired_speed: Vector3D) -> None:
        """Set the omni-directional speed action.

        Parameter
        ---------
        desired_speed : Vector3D
            The desired movement speed (x, y, theta).
        """

        self._desired_speed = desired_speed

    def get_desired_speed(self) -> Vector3D | None:
        """Retrieve the desired movement speed."""

        return self._desired_speed

    def commit(self, action: Action) -> None:
        if self._desired_speed is not None:
            action.put(OmniSpeedEffector(self.effector_name, self._desired_speed))

        # reset actuator
        self._desired_speed = None
