from dataclasses import dataclass

from magmapy.agent.communication.action import Effector
from magmapy.rchl.communication.rchl_mitecom import RCHLTeamMessage


@dataclass(frozen=True)
class RCHLTeamComEffector(Effector):
    """Effector for RCHL team communication."""

    message: RCHLTeamMessage
    """The team communication message."""
