from dataclasses import dataclass

from magma.agent.communication.action import Effector
from magma.rchl.communication.rchl_mitecom import RCHLTeamMessage


@dataclass(frozen=True)
class RCHLTeamComEffector(Effector):
    """Effector for RCHL team communication."""

    message: RCHLTeamMessage
    """The team communication message."""
