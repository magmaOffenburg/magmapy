from abc import ABC
from typing import Final

from magma.agent.model.robot.robot_model import PMutableRobotModel
from magma.rchl.model.rchl_agent import RCHLAgentModel
from magma.rchl.model.rchl_rules import RCHLRules
from magma.rchl.model.world.rchl_field_description import RCHLFieldVersion
from magma.soccer_agent.model.soccer_agent import PMutableSoccerAgentModel
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld, SoccerWorld
from magma.soccer_agent.runtime.soccer_factory import SoccerAgentFactory


class RCHLAgentFactory(SoccerAgentFactory, ABC):
    """Factory for RoboCup Humanoid League agent components."""

    def __init__(self, team_id: int, team_name: str, player_no: int, robot_model_id: str, field_version: str, decision_maker_id: str) -> None:
        """Construct a new RoboCup Humanoid League agent component factory.

        Parameter
        ---------
        team_id : int
            The id of our team in the Humanoid League.

        team_name : str
            The name of our team.

        player_no : int
            The player number.

        robot_model_id : str
            The robot model identifier.

        field_version : str
            The soccer field identifier.

        decision_maker_id : str
            The decision maker to use.
        """

        super().__init__(team_name, player_no, robot_model_id, field_version, decision_maker_id)

        self.team_id: Final[int] = team_id
        """The id of our team in the Humanoid League."""

    def _create_field_description(self) -> PSoccerFieldDescription:
        return RCHLFieldVersion.create_description_for(self.field_version)

    def _create_world(self, desc: PSoccerFieldDescription) -> PMutableSoccerWorld:
        return SoccerWorld(self.team_name, self.player_no, desc, 0.11)

    def _create_rule_book(self) -> SoccerRules:
        return RCHLRules()

    def _create_model(self, robot: PMutableRobotModel, world: PMutableSoccerWorld, rules: SoccerRules) -> PMutableSoccerAgentModel:
        return RCHLAgentModel(robot, world, rules, self.team_id)
