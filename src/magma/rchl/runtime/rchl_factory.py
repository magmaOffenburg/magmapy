from abc import ABC

from magma.rchl.model.rchl_rules import RCHLRules
from magma.rchl.model.world.rchl_field_description import RCHLFieldVersion
from magma.soccer_agent.model.soccer_rules import SoccerRules
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld, SoccerWorld
from magma.soccer_agent.runtime.soccer_factory import SoccerAgentFactory


class RCHLAgentFactory(SoccerAgentFactory, ABC):
    """
    Factory for RoboCup Humanoid League agent components.
    """

    def __init__(self, team_name: str, player_no: int, robot_model_id: str, field_version: str, decision_maker_id: str) -> None:
        """
        Construct a new RoboCup Humanoid League agent component factory.
        """

        super().__init__(team_name, player_no, robot_model_id, field_version, decision_maker_id)

    def _create_field_description(self) -> PSoccerFieldDescription:
        return RCHLFieldVersion.create_description_for(self._field_version)

    def _create_world(self, desc: PSoccerFieldDescription) -> PMutableSoccerWorld:
        return SoccerWorld(self._team_name, self._player_no, desc, 0.11)

    def _create_rule_book(self) -> SoccerRules:
        return RCHLRules()
