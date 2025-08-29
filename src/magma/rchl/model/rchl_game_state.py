from enum import Enum

from magma.soccer_agent.model.game_state import PlayMode, PlayModePhase


class RCHLGameTypes(Enum):
    """Game type constants."""

    UNKNOWN = -1
    """unknown game type."""

    ROUND_ROBIN = 0
    """Round-Robin game type."""

    PLAYOFF = 1
    """Playoff game type."""

    DROP_IN = 2
    """Drop-in game type."""


class RCHLGameStates(Enum):
    """State constants."""

    IMPOSSIBLE = -1
    """Well... impossible, isn't it?"""

    INITIAL = 0
    """The initial game state."""

    READY = 1
    """The ready game state."""

    SET = 2
    """The set game state."""

    PLAYING = 3
    """The playing / normal game state."""

    FINISHED = 4
    """The finished game state."""


class RCHLSecondaryGameStates(Enum):
    """Secondary state constants."""

    UNKNOWN = 255
    """Well... who knows?"""

    NORMAL = 0
    """The normal state."""

    PENALTY_SHOOT = 1
    """Penalty shoot state."""

    OVERTIME = 2
    """Playing overtime."""

    TIMEOUT = 3
    """Team / referee timeout."""

    DIRECT_FREE_KICK = 4
    """Direct free kick state."""

    INDIRECT_FREE_KICK = 5
    """Indirect free kick state."""

    PENALTY_KICK = 6
    """Penalty kick state."""

    CORNER_KICK = 7
    """Corner kicking."""

    GOAL_KICK = 8
    """Goal kick state."""

    THROW_IN = 9
    """Throw-in state."""


class RCHLSubModes(Enum):
    """Sub-modes constants (the secondary state info)."""

    FREEZE1 = 0
    """Freeze first."""

    READY = 1
    """Get ready."""

    FREEZE2 = 2
    """Freeze second."""


class RCHLTeamColors(Enum):
    """Team color constants."""

    BLUE = 0
    """The blue team."""

    RED = 1
    """The red team."""

    YELLOW = 2
    """The yellow team."""

    BLACK = 3
    """The black team."""

    WHITE = 4
    """The white team."""

    GREEN = 5
    """The green team."""

    ORANGE = 6
    """The orange team."""

    PURPLE = 7
    """The purple team."""

    BROWN = 8
    """The brown team."""

    GRAY = 9
    """The gray team."""


def decode_rchl_game_state(game_state: int, secondary_game_state: int, sub_mode: int, *, our_kick_off: bool, our_secondary_state: bool) -> tuple[PlayMode, PlayModePhase]:
    """Decode the given play mode and side into a game mode.

    Parameter
    ---------
    game_state : int
        The game controller state information.

    secondary_game_state : int
        The game controller secondary game state information.

    sub_mode : int
        The sub mode information of the secondary game state information.

    our_kick_off : bool
        Flag if our team has kick-off.

    our_secondary_state : bool
        Flag if the secondary state is for our team.
    """

    # check primary game state for INITIAL or FINISHED, which can be directly translated
    if game_state == RCHLGameStates.INITIAL.value:
        game_mode = PlayMode.TIMEOUT if secondary_game_state == RCHLSecondaryGameStates.TIMEOUT.value else PlayMode.BEFORE_KICK_OFF
        return game_mode, PlayModePhase.FREEZE

    if game_state == RCHLGameStates.FINISHED.value:
        return PlayMode.GAME_OVER, PlayModePhase.FREEZE

    # game states READY, SET or PLAYING --> check for secondary game state
    if secondary_game_state == RCHLSecondaryGameStates.CORNER_KICK.value:
        game_mode = PlayMode.OWN_CORNER_KICK if our_secondary_state else PlayMode.OPPONENT_CORNER_KICK
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state == RCHLSecondaryGameStates.DIRECT_FREE_KICK.value:
        game_mode = PlayMode.OWN_DIRECT_FREE_KICK if our_secondary_state else PlayMode.OPPONENT_DIRECT_FREE_KICK
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state == RCHLSecondaryGameStates.INDIRECT_FREE_KICK.value:
        game_mode = PlayMode.OWN_FREE_KICK if our_secondary_state else PlayMode.OPPONENT_FREE_KICK
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state == RCHLSecondaryGameStates.GOAL_KICK.value:
        game_mode = PlayMode.OWN_GOAL_KICK if our_secondary_state else PlayMode.OPPONENT_GOAL_KICK
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state == RCHLSecondaryGameStates.PENALTY_SHOOT.value:
        game_mode = PlayMode.OWN_PENALTY_SHOOT if our_kick_off else PlayMode.OPPONENT_PENALTY_SHOOT
        if game_state == RCHLGameStates.READY.value:
            return game_mode, PlayModePhase.PREPARATION

        if game_state == RCHLGameStates.SET.value:
            return game_mode, PlayModePhase.SET

        if game_state == RCHLGameStates.PLAYING.value:
            return game_mode, PlayModePhase.RUNNING

    if secondary_game_state == RCHLSecondaryGameStates.PENALTY_KICK.value:
        game_mode = PlayMode.OWN_PENALTY_KICK if our_secondary_state else PlayMode.OPPONENT_PENALTY_KICK
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state == RCHLSecondaryGameStates.THROW_IN.value:
        game_mode = PlayMode.OWN_THROW_IN if our_secondary_state else PlayMode.OPPONENT_THROW_IN
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state == RCHLSecondaryGameStates.DIRECT_FREE_KICK.value:
        game_mode = PlayMode.OWN_DIRECT_FREE_KICK if our_secondary_state else PlayMode.OPPONENT_DIRECT_FREE_KICK
        game_phase = PlayModePhase.PREPARATION if sub_mode == RCHLSubModes.READY.value else PlayModePhase.FREEZE
        return game_mode, game_phase

    if secondary_game_state in {RCHLSecondaryGameStates.NORMAL.value, RCHLSecondaryGameStates.OVERTIME.value}:
        if game_state == RCHLGameStates.READY.value:
            # TODO: if the kick-off-team-id is 128 the current play-mode of the game is in drop-ball, otherwise own- / opponent-kick-off
            return PlayMode.OWN_KICK_OFF if our_kick_off else PlayMode.OPPONENT_KICK_OFF, PlayModePhase.PREPARATION

        if game_state == RCHLGameStates.SET.value:
            # TODO: if the kick-off-team-id is 128 the current play-mode of the game is in drop-ball, otherwise own- / opponent-kick-off
            return PlayMode.OWN_KICK_OFF if our_kick_off else PlayMode.OPPONENT_KICK_OFF, PlayModePhase.SET

        if game_state == RCHLGameStates.PLAYING.value:
            return PlayMode.PLAY_ON, PlayModePhase.RUNNING

    return PlayMode.NONE, PlayModePhase.FREEZE
