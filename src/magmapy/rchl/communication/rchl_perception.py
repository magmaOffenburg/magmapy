from collections.abc import Sequence
from dataclasses import dataclass

from magmapy.agent.communication.perception import Perceptor
from magmapy.rchl.communication.rchl_mitecom import RCHLTeamMessage


@dataclass(frozen=True)
class SecondaryStateInfo:
    """Secondary game state information received from RCHL Game-Controller."""

    team_number: int
    """The TeamID relevant for the secondary state."""

    sub_mode: int
    """The secondary sub-state."""


@dataclass(frozen=True)
class RobotInfo:
    """Robot information received from RCHL Game-Controller."""

    penalty: int
    """The penalty state of the robot."""

    secs_till_unpenalised: int
    """Remaining seconds in current penalty state (if penalized)."""

    warning_count: int
    """Number of received warnings."""

    yellow_card_count: int
    """Number of received yellow cards."""

    red_card_count: int
    """Number of received red cards."""

    goalkeeper: bool
    """Flag if this player is goalkeeper (default player 1)."""


@dataclass(frozen=True)
class TeamInfo:
    """Team information received from RCHL Game-Controller."""

    team_number: int
    """The TeamID."""

    team_color: int
    """The team color."""

    score: int
    """The number of goals scored."""

    penalty_shot: int
    """The number of penalty shots taken."""

    single_shots: int
    """Bit-field, indicating successful / missed penalty shots."""

    players: Sequence[RobotInfo]
    """Sequence of player information."""


@dataclass(frozen=True)
class RCHLGameStatePerceptor(Perceptor):
    """Perceptor representing a RCHL soccer game state."""

    packet_number: int
    """Subsequent packet / message numbering."""

    player_per_team: int
    """The number of players per team."""

    game_type: int
    """The game type (round-robin, playoff, etc.)."""

    state: int
    """The current game state."""

    first_half: bool
    """Indicator for first half."""

    kick_off_team: int
    """The TeamID of the team that has kick-off."""

    secondary_state: int
    """The secondary state."""

    secondary_state_info: SecondaryStateInfo
    """Additional information to the secondary state."""

    drop_in_team: int
    """The TeamID in case of a drop-in game."""

    drop_in_time: int
    """???"""

    secs_remaining: int
    """Remaining time in seconds."""

    secondary_time: int
    """Secondary timer."""

    teams: Sequence[TeamInfo]
    """Sequence of team information messages."""


@dataclass(frozen=True)
class RCHLTeamComPerceptor(Perceptor):
    """Perceptor for RCHL team communication."""

    messages: Sequence[RCHLTeamMessage]
    """The team communication messages."""
