
from magma.agent.communication.channel_manager import DefaultChannelManager, PChannelManager
from magma.agent.decision.behavior import PBehavior
from magma.agent.decision.decision_maker import PDecisionMaker
from magma.agent.model.robot.robot_description import PRobotDescription
from magma.agent.model.robot.robot_model import PMutableRobotModel
from magma.rcss.communication.rcss_channel import RCSSServerChannel
from magma.rcss.decision.rcss_base_behaviors import CreateBehavior, InitBehavior
from magma.rcss.decision.rcss_decision_maker import RCSSDecisionMaker
from magma.rcss.model.rcss_rules import RCSSRules
from magma.rcss.model.robot.rcss_robot_description import (
    RCSSRobots,
)
from magma.rcss.model.robot.rcss_robot_model import RCSSRobotModel
from magma.rcss.model.world.rcss_field_description import (
    RCSSFieldVersion,
)
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld, SoccerWorld
from magma.soccer_agent.runtime.soccer_factory import SoccerAgentFactory


class RCSSAgentFactory(SoccerAgentFactory):
    """
    Factory for RoboCup Soccer Simulation agent components.
    """

    def __init__(self,
                 team_name: str,
                 player_no: int,
                 robot_model_id: str,
                 server_ip: str,
                 server_port: int,
                 field_version: str,
                 decision_maker_id: str) -> None:
        """
        Construct a new RoboCup Soccer Simulation agent component factory.
        """

        super().__init__(team_name, player_no, robot_model_id, field_version, decision_maker_id)

        self._server_ip: str = server_ip
        self._server_port: int = server_port

    def _create_channel_manager(self) -> PChannelManager:
        manager = DefaultChannelManager()

        # register channels
        manager.register_channel(RCSSServerChannel('RCSSChannel', self._server_ip, self._server_port))

        return manager

    def _create_robot_description(self) -> PRobotDescription:
        model_id = self._get_default_robot_model_id() if self._robot_model_id == 'default' else self._robot_model_id

        return RCSSRobots.create_description_for(model_id)

    def _get_default_robot_model_id(self) -> str:
        if self._player_no in (2, 5):
            return RCSSRobots.NAO0.value
        if self._player_no in (4, 6):
            return RCSSRobots.NAO2.value

        return RCSSRobots.NAO_TOE.value

    def _create_field_description(self) -> PSoccerFieldDescription:
        return RCSSFieldVersion.create_description_for(self._field_version)

    def _create_robot(self, desc: PRobotDescription) -> PMutableRobotModel:
        return RCSSRobotModel.from_description(desc)

    def _create_world(self, desc: PSoccerFieldDescription) -> PMutableSoccerWorld:
        return SoccerWorld(self._team_name, self._player_no, desc, 0.042)

    def _create_rule_book(self) -> SoccerRules:
        return RCSSRules()

    def _create_behaviors(self, model: PSoccerAgentModel) -> dict[str, PBehavior]:
        behaviors: dict[str, PBehavior] = super()._create_behaviors(model)

        def add_behavior(behavior: PBehavior) -> None:
            behaviors[behavior.get_name()] = behavior

        add_behavior(CreateBehavior(model))
        add_behavior(InitBehavior(model))

        return behaviors

    def _create_decision_maker(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> PDecisionMaker:
        return RCSSDecisionMaker(model, behaviors)
