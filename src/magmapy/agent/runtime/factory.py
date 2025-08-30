from typing import Protocol

from magmapy.agent.communication.channel_manager import PChannelManager
from magmapy.agent.decision.behavior import PBehavior
from magmapy.agent.decision.decision_maker import PDecisionMaker
from magmapy.agent.model.agent_model import PMutableAgentModel


class PAgentFactory(Protocol):
    """Protocol for an agent component factory."""

    def create_agent_components(self) -> tuple[PChannelManager, PMutableAgentModel, dict[str, PBehavior], PDecisionMaker]:
        """Create a set of core agent components."""
