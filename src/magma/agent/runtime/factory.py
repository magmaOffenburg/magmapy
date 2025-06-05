from typing import Protocol

from magma.agent.communication.channel_manager import PChannelManager
from magma.agent.decision.behavior import PBehavior
from magma.agent.decision.decision_maker import PDecisionMaker
from magma.agent.model.agent_model import PMutableAgentModel


class PAgentFactory(Protocol):
    """Protocol for an agent component factory."""

    def create_agent_components(self) -> tuple[PChannelManager, PMutableAgentModel, dict[str, PBehavior], PDecisionMaker]:
        """Create a set of core agent components."""
