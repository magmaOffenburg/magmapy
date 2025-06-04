from magma.agent.communication.channel_manager import DefaultChannelManager, PChannelManager
from magma.agent.communication.tcp_lpm_channel import TCPLPMChannel
from magma.agent.decision.behavior import PBehavior
from magma.agent.decision.decision_maker import PDecisionMaker
from magma.agent.model.robot.robot_description import PRobotDescription
from magma.agent.model.robot.robot_model import PMutableRobotModel
from magma.rcss.communication.rcss_msg_parser import RCSSMessageParser
from magma.rcss.communication.spark_msg_encoder import SimSparkMessageEncoder
from magma.rcss.decision.rcss_base_behaviors import InitBehavior
from magma.rcss.decision.rcss_decision_maker import RCSSDecisionMaker
from magma.rcss.model.rcss_rules import RCSSRules
from magma.rcss.model.robot.rcss_robot_model import RCSSRobotModel
from magma.rcss.model.robot.spark_robot_description import SimSparkRobots
from magma.rcss.model.world.rcss_field_description import RCSSFieldVersion
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld, SoccerWorld
from magma.soccer_agent.runtime.soccer_factory import SoccerAgentFactory


class SimSparkAgentFactory(SoccerAgentFactory):
    """
    Factory for RoboCup Soccer Simulation agent components.
    """

    def __init__(
        self,
        team_name: str,
        player_no: int,
        robot_model_id: str,
        server_ip: str,
        server_port: int,
        field_version: str,
        decision_maker_id: str,
    ) -> None:
        """
        Construct a new RoboCup Soccer Simulation agent component factory.
        """

        super().__init__(team_name, player_no, robot_model_id, field_version, decision_maker_id)

        self._server_ip: str = server_ip
        self._server_port: int = server_port

    def _create_channel_manager(self) -> PChannelManager:
        manager = DefaultChannelManager()

        # register channels
        manager.register_channel(TCPLPMChannel('SimSparkChannel', self._server_ip, self._server_port, RCSSMessageParser(), SimSparkMessageEncoder(), 4))

        return manager

    def _create_robot_description(self) -> PRobotDescription:
        model_id = self._get_default_robot_model_id() if self._robot_model_id == 'default' else self._robot_model_id

        return SimSparkRobots.create_description_for(model_id)

    def _get_default_robot_model_id(self) -> str:
        if self._player_no in (2, 5):
            return SimSparkRobots.NAO0.value
        if self._player_no in (4, 6):
            return SimSparkRobots.NAO2.value

        return SimSparkRobots.NAO_TOE.value

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

        add_behavior(InitBehavior(model))

        return behaviors

    def _create_decision_maker(self, model: PSoccerAgentModel, behaviors: dict[str, PBehavior]) -> PDecisionMaker:
        return RCSSDecisionMaker(model, behaviors)
