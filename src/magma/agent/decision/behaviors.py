from collections.abc import Mapping

from magma.agent.decision.behavior import Behavior, BehaviorID, PBehavior, PMoveBehavior, SingleComplexBehavior
from magma.agent.model.agent_model import PAgentModel
from magma.agent.model.robot.actuators import OmniSpeedActuator
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D


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

    def perform(self, *, stop: bool = False) -> None:
        # does intentionally nothing
        pass

    def is_finished(self) -> bool:
        return True


class MoveBehavior(Behavior):
    """Behavior for moving the robot."""

    def __init__(self, model: PAgentModel, name: str = BehaviorID.MOVE.value, actuator_name: str = 'move'):
        """Create a new move behavior.

        Parameter
        ---------
        model : PAgentModel
            The agent model instance.

        actuator_name : str, default='move'
            The name of the omni-speed actuator to use for commanding the requested movement speeds.
        """

        super().__init__(name)

        self._desired_movement_speed: Vector3D = V3D_ZERO
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

    def perform(self, *, stop: bool = False) -> None:
        if self._omni_speed_actuator is not None:
            if stop:
                self._desired_movement_speed = V3D_ZERO

            self._omni_speed_actuator.set(self._desired_movement_speed)

    def is_finished(self) -> bool:
        return True


class MoveReadyBehavior(SingleComplexBehavior):
    """Complex get-ready behavior based on the move behavior."""

    def __init__(
        self,
        behaviors: Mapping[str, PBehavior],
        name: str = BehaviorID.GET_READY.value,
    ):
        """Create a new get-ready behavior.

        Parameter
        ---------
        behaviors : Mapping[str, PBehavior]
            The map of known behaviors.

        name : str
            The unique name of the behavior.
        """

        super().__init__(name, behaviors)

        move_behavior = behaviors[BehaviorID.MOVE.value]
        self._move_behavior: PMoveBehavior | None = move_behavior if isinstance(move_behavior, PMoveBehavior) else None
        """The move-to behavior used to move to the desired pose."""

    def _decide_next(self) -> PBehavior | None:
        if self._move_behavior is None:
            # no move behavior available --> can't do anything
            return None

        # move zero
        self._move_behavior.set(V3D_ZERO)
        return self._move_behavior
