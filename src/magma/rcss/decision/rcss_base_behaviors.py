from __future__ import annotations

from typing import TYPE_CHECKING

from magma.agent.decision.behavior import Behavior, BehaviorID
from magma.rcss.model.robot.rcss_actuators import CreateActuator, InitActuator

if TYPE_CHECKING:
    from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


class InitBehavior(Behavior):
    """Behavior for creating and initializing an agent representation in simulation."""

    def __init__(self, model: PSoccerAgentModel):
        """Create a new init behavior.

        Parameter
        ---------
        model : PSoccerAgentModel
            The agent mode instance.
        """

        super().__init__(BehaviorID.INIT.value)

        self._model = model
        """The soccer agent model."""

        self._create_actuator: CreateActuator | None = self._model.get_robot().get_actuator('create', CreateActuator)
        """The create actuator in case a create action has to be performed."""

        self._init_actuator: InitActuator | None = self._model.get_robot().get_actuator('init', InitActuator)
        """The init actuator in case an init action has to be performed."""

    def perform(self) -> None:
        if self._create_actuator is not None:
            self._create_actuator.set()
            self._create_actuator = None

        elif self._init_actuator is not None:
            this_player = self._model.get_world().get_this_player()
            self._init_actuator.set(this_player.team_name, this_player.player_no)
            self._init_actuator = None

    def is_finished(self) -> bool:
        return self._create_actuator is None and self._init_actuator is None
