from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from magma.agent.model.agent_model import AgentModel, PAgentModel, PMutableAgentModel
from magma.soccer_agent.model.game_state import SoccerGameState

if TYPE_CHECKING:
    from magma.agent.communication.perception import Perception
    from magma.agent.model.robot.robot_model import PMutableRobotModel
    from magma.soccer_agent.model.game_state import PSoccerGameState
    from magma.soccer_agent.model.soccer_rules import SoccerRules
    from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld, PSoccerWorld


@runtime_checkable
class PSoccerAgentModel(PAgentModel, Protocol):
    """Base protocol for soccer agent models."""

    def get_world(self) -> PSoccerWorld:
        """Retrieve the current world state."""

    def get_game_state(self) -> PSoccerGameState:
        """Retrieve the current soccer game state."""

    def get_game_rules(self) -> SoccerRules:
        """Retrieve the soccer game rule book."""


@runtime_checkable
class PMutableSoccerAgentModel(PSoccerAgentModel, PMutableAgentModel, Protocol):
    """Base protocol for mutable soccer agent models."""


class SoccerAgentModel(AgentModel, ABC):
    """The soccer agent model."""

    def __init__(
        self,
        robot: PMutableRobotModel,
        world: PMutableSoccerWorld,
        rules: SoccerRules,
    ) -> None:
        """Construct a new soccer agent model.

        Parameter
        ---------
        robot : PMutableRobotModel
            The robot model representation.

        world : PMutableSoccerWorld
            The soccer world model.

        rules : SoccerRules
            The soccer rule book.
        """

        super().__init__(robot)

        self._world: PMutableSoccerWorld = world
        """The soccer world representation."""

        self._game_state: SoccerGameState = SoccerGameState(world.get_this_player().team_name)
        """The soccer game state."""

        self._game_rules: SoccerRules = rules
        """The soccer rule book."""

    def get_world(self) -> PSoccerWorld:
        """Retrieve the current world state."""

        return self._world

    def get_game_state(self) -> PSoccerGameState:
        """Retrieve the current soccer game state."""

        return self._game_state

    def get_game_rules(self) -> SoccerRules:
        """Retrieve the soccer game rule book."""

        return self._game_rules

    def update(self, perception: Perception) -> None:
        """Update the state of the agent model from the given perceptions.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """

        # process perceptions
        # 1: update global time
        self._update_global_time(perception)

        # 2: update sensor states
        self._update_robot_model(perception)

        # 3: update game state
        self._update_game_state(perception)

        # 4: update world state
        self._update_world(perception)

        # 5: update state of beliefs
        self._update_beliefs()

    @abstractmethod
    def _update_game_state(self, perception: Perception) -> None:
        """Update the game state model from the given perception.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """

    def _update_world(self, perception: Perception) -> None:
        """Update the world state from the given perception.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """

        self._world.update(perception, self._robot)
