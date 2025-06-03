from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magma.agent.model.base import PMutableModel

if TYPE_CHECKING:
    from magma.agent.communication.action import Action
    from magma.agent.communication.perception import Perception
    from magma.agent.model.belief import Belief, PBelief
    from magma.agent.model.robot.robot_model import PMutableRobotModel, PRobotModel


@runtime_checkable
class PAgentModel(Protocol):
    """
    Protocol for agent models.
    """

    def get_time(self) -> float:
        """
        Retrieve the current time.
        """

    def get_robot(self) -> PRobotModel:
        """
        Retrieve the robot model.
        """

    def get_belief(self, name: str) -> PBelief | None:
        """
        Retrieve the belief with the given name.
        """


@runtime_checkable
class PMutableAgentModel(PAgentModel, PMutableModel, Protocol):
    """
    Protocol for mutable agent models.
    """

    def get_robot(self) -> PMutableRobotModel:
        """
        Retrieve the robot model.
        """

    def generate_action(self) -> Action:
        """
        Generate a set of actions from all available actuators of the robot model.
        """


class AgentModel:
    """
    Base implementation for agent models.
    """

    def __init__(self, robot: PMutableRobotModel) -> None:
        """
        Create a new agent model.
        """

        self._time: float = 0
        self._robot: Final[PMutableRobotModel] = robot
        self._beliefs: Final[dict[str, Belief]] = {}

    def get_time(self) -> float:
        """
        Retrieve the current time.
        """

        return self._time

    def get_robot(self) -> PMutableRobotModel:
        """
        Retrieve the robot model.
        """

        return self._robot

    def get_belief(self, name: str) -> PBelief | None:
        """
        Retrieve the belief with the given name.
        """

        return self._beliefs.get(name, None)

    def update(self, perception: Perception) -> None:
        """
        Update the state of the agent model from the given perceptions.
        """

        # process perceptions
        # 1: update global time
        self._update_global_time(perception)

        # 2: update sensor states
        self._update_robot_model(perception)

        # 3: update state of beliefs
        self._update_beliefs()

    def _update_global_time(self, perception: Perception) -> None:
        """
        Update the global time from the given perceptions.
        """

        self._time = perception.get_time()

    def _update_robot_model(self, perception: Perception) -> None:
        """
        Update the robot model from the given perceptions.
        """

        self._robot.update(perception)

    def _update_beliefs(self) -> None:
        """
        Update the state of beliefs.
        """

        for belief in self._beliefs.values():
            belief.update()

    def generate_action(self) -> Action:
        """
        Generate a set of actions from all available actuators of the robot model.
        """

        return self._robot.generate_action()
