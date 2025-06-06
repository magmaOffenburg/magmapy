from abc import ABC, abstractmethod

from magma.agent.communication.channel_manager import PChannelManager
from magma.agent.decision.behavior import PBehavior
from magma.agent.decision.behaviors import NoneBehavior
from magma.agent.decision.decision_maker import PDecisionMaker
from magma.agent.model.robot.robot_description import PRobotDescription
from magma.agent.model.robot.robot_model import PMutableRobotModel, RobotModel
from magma.soccer_agent.model.game_state import PMutableSoccerGameState, SoccerGameState
from magma.soccer_agent.model.soccer_agent import PMutableSoccerAgentModel, PSoccerAgentModel, SoccerAgentModel
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld


class SoccerAgentFactory(ABC):
    """
    Factory for soccer agent components.
    """

    def __init__(
        self,
        team_name: str,
        player_no: int,
        robot_model_id: str,
        field_version: str,
        decision_maker_id: str,
    ) -> None:
        """
        Construct a new soccer agent component factory.
        """

        self._team_name: str = team_name
        self._player_no: int = player_no
        self._robot_model_id: str = robot_model_id
        self._field_version: str = field_version
        self._decision_maker_id: str = decision_maker_id

    def create_agent_components(self) -> tuple[PChannelManager, PMutableSoccerAgentModel, dict[str, PBehavior], PDecisionMaker]:
        """
        Create a set of core agent components.
        """

        channel_manager: PChannelManager = self._create_channel_manager()
        model: PMutableSoccerAgentModel = self._create_model()
        behaviors: dict[str, PBehavior] = self._create_behaviors(model)
        decision: PDecisionMaker = self._create_decision_maker(model, behaviors)

        return (channel_manager, model, behaviors, decision)

    @abstractmethod
    def _create_channel_manager(self) -> PChannelManager:
        """
        Create the channel manager component.
        """

    def _create_model(self) -> PMutableSoccerAgentModel:
        """
        Create the agent models.
        """

        robot_desc: PRobotDescription = self._create_robot_description()
        field_desc: PSoccerFieldDescription = self._create_field_description()

        robot: PMutableRobotModel = self._create_robot(robot_desc)
        world: PMutableSoccerWorld = self._create_world(field_desc)
        game_state: PMutableSoccerGameState = self._create_game_state()
        rules: SoccerRules = self._create_rule_book()

        return SoccerAgentModel(robot, world, game_state, rules)

    @abstractmethod
    def _create_robot_description(self) -> PRobotDescription:
        """
        Create the robot description.
        """

    @abstractmethod
    def _create_field_description(self) -> PSoccerFieldDescription:
        """
        Create the soccer field description.
        """

    def _create_robot(self, desc: PRobotDescription) -> PMutableRobotModel:
        """
        Create the robot.
        """

        return RobotModel.from_description(desc)

    @abstractmethod
    def _create_world(self, desc: PSoccerFieldDescription) -> PMutableSoccerWorld:
        """
        Create the soccer world.
        """

    def _create_game_state(self) -> PMutableSoccerGameState:
        """
        Create the game state model.
        """

        return SoccerGameState(self._team_name)

    @abstractmethod
    def _create_rule_book(self) -> SoccerRules:
        """
        Create the soccer rule book.
        """

    def _create_behaviors(self, model: PSoccerAgentModel) -> dict[str, PBehavior]:
        """
        Create the agent specific behaviors.
        """

        del model  # not used in this method

        behaviors: dict[str, PBehavior] = {}

        def add_behavior(behavior: PBehavior) -> None:
            behaviors[behavior.name] = behavior

        add_behavior(NoneBehavior())

        return behaviors

    @abstractmethod
    def _create_decision_maker(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> PDecisionMaker:
        """
        Create the channel manager component.
        """
