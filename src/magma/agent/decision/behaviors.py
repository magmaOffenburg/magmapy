from typing import Protocol, runtime_checkable

from magma.agent.decision.behavior import Behavior, BehaviorID, PBehavior
from magma.agent.model.agent_model import PAgentModel
from magma.agent.model.robot.actuators import OmniSpeedActuator
from magma.common.math.geometry.vector import Vector3D


@runtime_checkable
class PMoveBehavior(Protocol, PBehavior):
    """Protocol for move behaviors."""

    def set(self, desired_speed: Vector3D) -> None:
        """Set the desired movement speed.

        Parameter
        ---------
        desired_speed : Vector3D
            The desired movement speed vector (x, y, theta).
        """


class NoneBehavior(Behavior):
    """A behavior that does nothing."""

    def __init__(self, name: str = BehaviorID.NONE.value) -> None:
        """Construct a new none-behavior.

        Parameter
        ---------
        name : str, default=BehaviorID.NONE.value
            The name of the behavior.
        """

        super().__init__(name)

    def perform(self) -> None:
        # does intentionally nothing
        pass

    def is_finished(self) -> bool:
        return True


class MoveBehavior(Behavior):
    """Behavior for moving the robot."""

    def __init__(self, model: PAgentModel, actuator_name: str = 'move'):
        """Create a new move behavior.

        Parameter
        ---------
        model : PAgentModel
            The agent model instance.

        actuator_name : str, default='move'
            The name of the omni-speed actuator to use for commanding the requested movement speeds.
        """

        super().__init__(BehaviorID.MOVE.value)

        self._desired_movement_speed: Vector3D = Vector3D(0, 0, 0)
        """The desired movement speed (x, y, theta)."""

        self._omni_speed_actuator: OmniSpeedActuator | None = model.get_robot().get_actuator(actuator_name, OmniSpeedActuator)
        """The omni-directional movement speed actuator used to command requested movement speeds."""

        if self._omni_speed_actuator is None:
            print(f'WARNING: Robot model has no omni-speed actuator with the name "{actuator_name}"!')  # noqa: T201

    def set(self, desired_speed: Vector3D) -> None:
        """Set the desired movement speed.

        Parameter
        ---------
        desired_speed : Vector3D
            the desired movement speed vector (x, y, theta).
        """

        self._desired_movement_speed = desired_speed

    def perform(self) -> None:
        if self._omni_speed_actuator is not None:
            self._omni_speed_actuator.set(self._desired_movement_speed)

    def is_finished(self) -> bool:
        return True
