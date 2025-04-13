from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from magma.agent.decision.behavior import Behavior
from magma.rcss.model.robot.rcss_actuators import CreateActuator, InitActuator

if TYPE_CHECKING:
    from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


class RCSSBehaviorID(Enum):
    """
    Enum specifying soccer behavior names.
    """

    CREATE = 'create'
    """
    The create behavior used to spawn a robot in simulation.
    """

    INIT = 'init'
    """
    The init behavior used to initialize a robot in simulation.
    """


class CreateBehavior(Behavior):
    """
    Behavior for creating / spawning an agent representation in simulation.
    """

    def __init__(self, model: PSoccerAgentModel):
        """
        Create a new create behavior.
        """

        super().__init__(RCSSBehaviorID.CREATE.value)

        self._model = model

        self._create_actuator: CreateActuator | None = self._model.get_robot().get_actuator('create', CreateActuator)
        self._creation_completed: bool = False

        if self._create_actuator is None:
            self._creation_completed = True
            print('WARNING: Robot model has no create actuator with the name "create"!')  # noqa: T201

    def perform(self) -> None:
        if not self._creation_completed:
            if self._create_actuator is not None:
                self._create_actuator.set()
            self._creation_completed = True

    def is_finished(self) -> bool:
        return self._creation_completed


class InitBehavior(Behavior):
    """
    Behavior for initializing an agent representation in simulation.
    """

    def __init__(self, model: PSoccerAgentModel):
        """
        Create a new init behavior.
        """

        super().__init__(RCSSBehaviorID.INIT.value)

        self._model = model

        self._init_actuator: InitActuator | None = self._model.get_robot().get_actuator('init', InitActuator)
        self._initialization_completed: bool = False

        if self._init_actuator is None:
            self._initialization_completed = True
            print('WARNING: Robot model has no initialization actuator with the name "init"!')  # noqa: T201

    def perform(self) -> None:
        if not self._initialization_completed:
            if self._init_actuator is not None:
                this_player = self._model.get_world().get_this_player()
                self._init_actuator.set(this_player.get_team(), this_player.get_player_no())
            self._initialization_completed = True

    def is_finished(self) -> bool:
        return self._initialization_completed
