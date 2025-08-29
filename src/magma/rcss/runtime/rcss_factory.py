from magma.agent.communication.channel_manager import DefaultChannelManager, PChannelManager
from magma.agent.communication.tcp_lpm_channel import TCPLPMChannel
from magma.agent.decision.behavior import PBehavior
from magma.agent.model.robot.robot_description import PRobotDescription
from magma.agent.model.robot.robot_model import PMutableRobotModel
from magma.rcss.communication.rcss_msg_encoder import RCSSMessageEncoder
from magma.rcss.communication.rcss_msg_parser import RCSSMessageParser
from magma.rcss.decision.rcss_base_behaviors import InitBehavior
from magma.rcss.model.rcss_agent import RCSSAgentModel
from magma.rcss.model.rcss_rules import RCSSRules
from magma.rcss.model.robot.rcss_robot_model import RCSSRobotModel
from magma.rcss.model.robot.rcss_robots import RCSSRobots
from magma.rcss.model.world.rcss_field_description import RCSSFieldVersion
from magma.rcss.model.world.rcss_soccer_world import RCSSSoccerWorld
from magma.soccer_agent.model.soccer_agent import PMutableSoccerAgentModel, PSoccerAgentModel
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.strategy.role_manager import PMutableRoleManager
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld
from magma.soccer_agent.runtime.soccer_factory import SoccerAgentFactory


class RCSSAgentFactory(SoccerAgentFactory):
    """Factory for RoboCup Soccer Simulation (MuJoCo) agent components."""

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
        """Construct a new RoboCup Soccer Simulation agent component factory."""

        super().__init__(team_name, player_no, robot_model_id, field_version, decision_maker_id)

        self._server_ip: str = server_ip
        self._server_port: int = server_port

    def _create_channel_manager(self) -> PChannelManager:
        manager = DefaultChannelManager()

        # register channels
        manager.register_channel(TCPLPMChannel('RCSSSMJChannel', self._server_ip, self._server_port, RCSSMessageParser(), RCSSMessageEncoder(), 4))

        return manager

    def _create_robot_description(self) -> PRobotDescription:
        model_id = self._get_default_robot_model_id() if self.robot_model_id == 'default' else self.robot_model_id

        return RCSSRobots.create_description_for(model_id)

    def _get_default_robot_model_id(self) -> str:
        return RCSSRobots.T1.value

    def _create_field_description(self) -> PSoccerFieldDescription:
        return RCSSFieldVersion.create_description_for(self.field_version)

    def _create_robot(self, desc: PRobotDescription) -> PMutableRobotModel:
        return RCSSRobotModel.from_description(desc)

    def _create_world(self, desc: PSoccerFieldDescription) -> PMutableSoccerWorld:
        return RCSSSoccerWorld(self.team_name, self.player_no, desc, 0.11)

    def _create_rule_book(self) -> SoccerRules:
        return RCSSRules()

    def _create_model(
        self,
        robot: PMutableRobotModel,
        world: PMutableSoccerWorld,
        rules: SoccerRules,
        role_manager: PMutableRoleManager,
    ) -> PMutableSoccerAgentModel:
        return RCSSAgentModel(robot, world, rules, role_manager)

    def _create_behaviors(self, model: PSoccerAgentModel) -> dict[str, PBehavior]:
        behaviors: dict[str, PBehavior] = super()._create_behaviors(model)

        def add_behavior(behavior: PBehavior) -> None:
            behaviors[behavior.name] = behavior

        add_behavior(InitBehavior(model))

        return behaviors
