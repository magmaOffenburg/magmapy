from __future__ import annotations

from typing import TYPE_CHECKING

from magmapy.agent.decision.behavior import Behavior, BehaviorID
from magmapy.rcss.model.robot.rcss_actuators import InitActuator

if TYPE_CHECKING:
    from magmapy.soccer_agent.model.soccer_agent import PSoccerAgentModel


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

        self._init_actuator: InitActuator | None = self._model.get_robot().get_actuator('init', InitActuator)
        """The init actuator in case an init action has to be performed."""

    def perform(self, *, stop: bool = False) -> None:
        if self._init_actuator is not None:
            this_player = self._model.get_world().get_this_player()
            self._init_actuator.set(this_player.team_name, this_player.player_no)
            self._init_actuator = None

    def is_finished(self) -> bool:
        return self._init_actuator is None
