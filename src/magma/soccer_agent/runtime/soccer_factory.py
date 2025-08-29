from abc import ABC, abstractmethod
from typing import Final

from magma.agent.communication.channel_manager import PChannelManager
from magma.agent.decision.behavior import PBehavior
from magma.agent.decision.behaviors import NoneBehavior
from magma.agent.decision.decision_maker import PDecisionMaker
from magma.agent.model.robot.robot_description import PRobotDescription
from magma.agent.model.robot.robot_model import PMutableRobotModel, RobotModel
from magma.soccer_agent.decision.soccer_decision_maker import SoccerDecisionMaker
from magma.soccer_agent.model.soccer_agent import PMutableSoccerAgentModel, PSoccerAgentModel
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.strategy.role_assignment import PRoleAssignmentStrategy, RoleAssignmentStrategy
from magma.soccer_agent.model.strategy.role_manager import PMutableRoleManager, RoleManager
from magma.soccer_agent.model.strategy.strategies import DEFAULT_11_VS_11_STRATEGY
from magma.soccer_agent.model.strategy.strategy import PStrategyBook, SingletonStrategyBook
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

        self.team_name: Final[str] = team_name
        self.player_no: Final[int] = player_no
        self.robot_model_id: Final[str] = robot_model_id
        self.field_version: Final[str] = field_version
        self.decision_maker_id: Final[str] = decision_maker_id

    def create_agent_components(self) -> tuple[PChannelManager, PMutableSoccerAgentModel, dict[str, PBehavior], PDecisionMaker]:
        """
        Create a set of core agent components.
        """

        # communication
        channel_manager: PChannelManager = self._create_channel_manager()

        # model
        robot_desc: PRobotDescription = self._create_robot_description()
        field_desc: PSoccerFieldDescription = self._create_field_description()

        robot: PMutableRobotModel = self._create_robot(robot_desc)
        world: PMutableSoccerWorld = self._create_world(field_desc)
        rules: SoccerRules = self._create_rule_book()
        role_manager: PMutableRoleManager = self._create_role_manager()
        model: PMutableSoccerAgentModel = self._create_model(robot, world, rules, role_manager)

        # decision
        behaviors: dict[str, PBehavior] = self._create_behaviors(model)
        decision: PDecisionMaker = self._create_decision_maker(model, behaviors)

        return (channel_manager, model, behaviors, decision)

    @abstractmethod
    def _create_channel_manager(self) -> PChannelManager:
        """
        Create the channel manager component.
        """

    @abstractmethod
    def _create_model(
        self,
        robot: PMutableRobotModel,
        world: PMutableSoccerWorld,
        rules: SoccerRules,
        role_manager: PMutableRoleManager,
    ) -> PMutableSoccerAgentModel:
        """
        Create the agent model.
        """

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

    @abstractmethod
    def _create_rule_book(self) -> SoccerRules:
        """
        Create the soccer rule book.
        """

    def _create_role_manager(self) -> PMutableRoleManager:
        """
        Create the soccer role manager.
        """

        strategy_book = self._create_strategy_book()
        role_assignment = self._create_role_assignment_strategy()

        return RoleManager(strategy_book, role_assignment)

    def _create_strategy_book(self) -> PStrategyBook:
        """
        Create the soccer strategy book.
        """

        return SingletonStrategyBook(DEFAULT_11_VS_11_STRATEGY)

    def _create_role_assignment_strategy(self) -> PRoleAssignmentStrategy:
        """
        Create the soccer role assignment strategy.
        """

        return RoleAssignmentStrategy()

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

    def _create_decision_maker(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> PDecisionMaker:
        """
        Create the decision maker component.
        """

        return SoccerDecisionMaker(model, behaviors)
