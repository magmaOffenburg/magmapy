from enum import Enum

from magmapy.soccer_agent.model.game_state import PlayMode, PlayModePhase, PlaySide


class RCSSPlayModes(Enum):
    """Secondary state constants."""

    BEFORE_KICK_OFF = 'BeforeKickOff'

    KICK_OFF_LEFT = 'KickOff_Left'

    KICK_OFF_RIGHT = 'KickOff_Right'

    PLAY_ON = 'PlayOn'

    KICK_IN_LEFT = 'KickIn_Left'

    KICK_IN_RIGHT = 'KickIn_Right'

    CORNER_KICK_LEFT = 'corner_kick_left'

    CORNER_KICK_RIGHT = 'corner_kick_right'

    GOAL_KICK_LEFT = 'goal_kick_left'

    GOAL_KICK_RIGHT = 'goal_kick_right'

    OFFSIDE_LEFT = 'offside_left'

    OFFSIDE_RIGHT = 'offside_right'

    GAME_OVER = 'GameOver'

    GOAL_LEFT = 'Goal_Left'

    GOAL_RIGHT = 'Goal_Right'

    FREE_KICK_LEFT = 'free_kick_left'

    FREE_KICK_RIGHT = 'free_kick_right'

    DIRECT_FREE_KICK_LEFT = 'direct_free_kick_left'

    DIRECT_FREE_KICK_RIGHT = 'direct_free_kick_right'

    NONE = 'NONE'

    PENALTY_KICK_LEFT = 'penalty_kick_left'

    PENALTY_KICK_RIGHT = 'penalty_kick_right'

    PENALTY_SHOOT_LEFT = 'penalty_shoot_left'

    PENALTY_SHOOT_RIGHT = 'penalty_shoot_right'


def decode_rcss_play_mode(play_mode: str, play_side: PlaySide) -> tuple[PlayMode, PlayModePhase]:
    """Decode the given play mode and side into a game mode.

    Parameter
    ---------
    play_mode : str
        The server play mode.

    play_side : PlaySide
        Our play side.
    """

    left_side: bool = play_side == PlaySide.LEFT

    if play_mode == RCSSPlayModes.BEFORE_KICK_OFF.value:
        return PlayMode.BEFORE_KICK_OFF, PlayModePhase.PREPARATION

    if play_mode == RCSSPlayModes.KICK_OFF_LEFT.value:
        return PlayMode.OWN_KICK_OFF if left_side else PlayMode.OPPONENT_KICK_OFF, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.KICK_OFF_RIGHT.value:
        return PlayMode.OPPONENT_KICK_OFF if left_side else PlayMode.OWN_KICK_OFF, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.PLAY_ON.value:
        return PlayMode.PLAY_ON, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.KICK_IN_LEFT.value:
        return PlayMode.OWN_THROW_IN if left_side else PlayMode.OPPONENT_THROW_IN, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.KICK_IN_RIGHT.value:
        return PlayMode.OPPONENT_THROW_IN if left_side else PlayMode.OWN_THROW_IN, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.CORNER_KICK_LEFT.value:
        return PlayMode.OWN_CORNER_KICK if left_side else PlayMode.OPPONENT_CORNER_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.CORNER_KICK_RIGHT.value:
        return PlayMode.OPPONENT_CORNER_KICK if left_side else PlayMode.OWN_CORNER_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.GOAL_KICK_LEFT.value:
        return PlayMode.OWN_GOAL_KICK if left_side else PlayMode.OPPONENT_GOAL_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.GOAL_KICK_RIGHT.value:
        return PlayMode.OPPONENT_GOAL_KICK if left_side else PlayMode.OWN_GOAL_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.OFFSIDE_LEFT.value:
        return PlayMode.OWN_FREE_KICK if left_side else PlayMode.OPPONENT_FREE_KICK, PlayModePhase.PREPARATION

    if play_mode == RCSSPlayModes.OFFSIDE_RIGHT.value:
        return PlayMode.OPPONENT_FREE_KICK if left_side else PlayMode.OWN_FREE_KICK, PlayModePhase.PREPARATION

    if play_mode == RCSSPlayModes.GAME_OVER.value:
        return PlayMode.GAME_OVER, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.GOAL_LEFT.value:
        return PlayMode.OPPONENT_KICK_OFF if left_side else PlayMode.OWN_KICK_OFF, PlayModePhase.PREPARATION

    if play_mode == RCSSPlayModes.GOAL_RIGHT.value:
        return PlayMode.OWN_KICK_OFF if left_side else PlayMode.OPPONENT_KICK_OFF, PlayModePhase.PREPARATION

    if play_mode == RCSSPlayModes.FREE_KICK_LEFT.value:
        return PlayMode.OWN_FREE_KICK if left_side else PlayMode.OPPONENT_FREE_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.FREE_KICK_RIGHT.value:
        return PlayMode.OPPONENT_FREE_KICK if left_side else PlayMode.OWN_FREE_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.DIRECT_FREE_KICK_LEFT.value:
        return PlayMode.OWN_DIRECT_FREE_KICK if left_side else PlayMode.OPPONENT_DIRECT_FREE_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.DIRECT_FREE_KICK_RIGHT.value:
        return PlayMode.OPPONENT_DIRECT_FREE_KICK if left_side else PlayMode.OWN_DIRECT_FREE_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.NONE.value:
        return PlayMode.NONE, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.PENALTY_KICK_LEFT.value:
        return PlayMode.OWN_PENALTY_KICK if left_side else PlayMode.OPPONENT_PENALTY_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.PENALTY_KICK_RIGHT.value:
        return PlayMode.OPPONENT_PENALTY_KICK if left_side else PlayMode.OWN_PENALTY_KICK, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.PENALTY_SHOOT_LEFT.value:
        return PlayMode.OWN_PENALTY_SHOOT if left_side else PlayMode.OPPONENT_PENALTY_SHOOT, PlayModePhase.RUNNING

    if play_mode == RCSSPlayModes.PENALTY_SHOOT_RIGHT.value:
        return PlayMode.OPPONENT_PENALTY_SHOOT if left_side else PlayMode.OWN_PENALTY_SHOOT, PlayModePhase.RUNNING

    # print("WARNING: Unknown play mode: \"" + play_mode + "\"!")

    return PlayMode.NONE, PlayModePhase.SET
