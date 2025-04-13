from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Protocol

from magma.agent.model.base import PMutableModel
from magma.soccer_agent.communication.soccer_perception import SoccerGameStatePerceptor

if TYPE_CHECKING:
    from magma.agent.communication.perception import Perception


class PlaySide(Enum):
    """
    Enum specifying the different play side options in a soccer game,
    """

    UNKNOWN = "unknown"
    """
    We play from left to right.
    """

    LEFT = "left"
    """
    We play from left to right.
    """

    RIGHT = "right"
    """
    We play from right to left.
    """

    @staticmethod
    def from_value(side_id: str) -> PlaySide:
        """
        Fetch the enum entry corresponding to the given side identifier.
        """

        side_id = side_id.lower()

        for v in PlaySide:
            if v.value == side_id:
                return v

        # print("WARNING: Unknown Play Side: \"" + side_id + "\"!")

        return PlaySide.UNKNOWN


class SoccerGameMode(Enum):
    """
    Enum specifying the different game modes of a soccer game (tailored towards RoboCup leagues).
    """

    NONE = "none"
    """
    No game mode or an unknown one (should not be used!).
    """

    FREEZE = "freeze"
    """
    Don't move!

    The game is freezed / on hold and nobody should actively move around.
    """

    BEFORE_KICK_OFF = "before-kick-off"
    """
    The game has not started yet.

    Players may position themselves on their half of the soccer field.
    """

    GAME_OVER = "game-over"
    """
    The game is over.
    """

    OWN_KICK_OFF = "own-kick-off"
    """
    Kick-off for our team.

    The ball is in the center, and our team is allowed to kick it first.
    """

    OPPONENT_KICK_OFF = "opponent-kick-off"
    """
    Kick-off for the opponent team.

    The ball is in the center, and the opponent team is allowed to kick it.
    """

    PLAY_ON = "play-on"
    """
    Normal gameplay.

    The game is processing normally, no special rules are in place.
    """

    OWN_GOAL_KICK = "own-goal-kick"
    """
    Goal-kick for our team.

    The opponent team kicked the ball outside the play field across our side line and our team is allowed to perform a goal kick (kick-off from goal).
    """

    OPPONENT_GOAL_KICK = "opponent-goal-kick"
    """
    Goal-kick for the opponent team.

    Our team kicked the ball outside the play field across the opponent side line and the opponent team is allowed to perform a goal kick (kick-off from goal).
    """

    OWN_THROW_IN = "own-throw-in"
    """
    Throw-in for our team.

    The opponent team has kicked the ball outside the play field across the upper / lower ground line and our team is allowed to throw / kick it back into the field.
    """

    OPPONENT_THROW_IN = "opponent-throw-in"
    """
    Throw-in for the opponent team.

    Our team has kicked the ball outside the play field across the upper / lower ground line and the opponent team is allowed to throw / kick it back into the field.
    """

    OWN_CORNER_KICK = "own-corner-kick"
    """
    Corner-kick for our team.

    The opponent team kicked the ball outside the play field across their side line and our team is allowed to perform a corner kick.
    """

    OPPONENT_CORNER_KICK = "opponent-corner-kick"
    """
    Corner-kick for the opponent team.

    Our team kicked the ball outside the play field across our side line and the opponent team is allowed to perform a corner kick.
    """

    OWN_FREE_KICK = "own-free-kick"
    """
    Indirect free-kick for our team.

    Our team got an indirect free kick and may kick the ball first.
    """

    OPPONENT_FREE_KICK = "opponent-free-kick"
    """
    Indirect free-kick for the opponent team.

    The opponent team got an indirect free kick and may kick the ball first.
    """

    OWN_DIRECT_FREE_KICK = "own-direct-free-kick"
    """
    Direct free-kick for our team.

    Our team got a direct free kick and may kick the ball first.
    """

    OPPONENT_DIRECT_FREE_KICK = "opponent-direct-free-kick"
    """
    Direct free-kick for the opponent team.

    The opponent team got a direct free kick and may kick the ball first.
    """

    OWN_PENALTY_KICK = "own-penalty-kick"
    """
    Penalty-kick for our team.

    Our team should perform a penalty kick. The ball is at the penalty spot in front of the opponent goal.
    """

    OPPONENT_PENALTY_KICK = "opponent-penalty-kick"
    """
    Penalty-kick for the opponent team.

    The opponent team should perform a penalty kick. The ball is at the penalty spot in front of our goal.
    """

    OWN_PENALTY_SHOOT = "own-penalty-shoot"
    """
    Penalty-shoot for our team.

    Our team should perform a penalty shootout by somehow dribbling / kicking the ball into the opponent goal. The ball is initially at the center of the field.
    """

    OPPONENT_PENALTY_SHOOT = "opponent-penalty-shoot"
    """
    Penalty-shoot for the opponent team.

    The opponent team should perform a penalty shootout by somehow dribbling / kicking the ball into our goal. The ball is initially at the center of the field.
    """

    OWN_PASS = "own-pass" # noqa: S105 - Prevent ruff hardcoded-passwort-assignment warning
    """
    Pass-mode for our team.

    Our team has exclusive access to the ball for passing, while the opponent team players are not allowed to get too close to the ball.
    """

    OPPONENT_PASS = "opponent-pass" # noqa: S105 - Prevent ruff hardcoded-passwort-assignment warning
    """
    Pass-mode for the opponent team.

    The opponent team has exclusive access to the ball for passing, while our team players are not allowed to get too close to the ball.
    """

    OWN_OFFSIDE = "own-offside"
    """
    Offside in favour of our team.

    The opponent team violated the offside rule and our team is allowed to kick the ball first.
    """

    OPPONENT_OFFSIDE = "opponent-offside"
    """
    Offside in favour of the opponent team.

    Our team violated the offside rule and the opponent team is allowed to kick the ball first.
    """

    OWN_GOAL = "own-goal"
    """
    Our team scored a goal.

    A goal was counted for our team and everybody can celebrate.
    """

    OPPONENT_GOAL = "opponent-goal"
    """
    The opponent team scored a goal.

    A goal was counted for the opponent team. Should not happen... team! Get your stuff together!
    """


def decode_rcss_game_mode(play_mode: str, play_side: PlaySide) -> SoccerGameMode:
    """
    Decode the given play mode and side into a game mode.
    """

    left_side: bool = play_side == PlaySide.LEFT

    if play_mode == "BeforeKickOff":
        return SoccerGameMode.BEFORE_KICK_OFF
    if play_mode == "KickOff_Left":
        return SoccerGameMode.OWN_KICK_OFF if left_side else SoccerGameMode.OPPONENT_KICK_OFF
    if play_mode == "KickOff_Right":
        return SoccerGameMode.OPPONENT_KICK_OFF if left_side else SoccerGameMode.OWN_KICK_OFF
    if play_mode == "PlayOn":
        return SoccerGameMode.PLAY_ON
    if play_mode == "KickIn_Left":
        return SoccerGameMode.OWN_THROW_IN if left_side else SoccerGameMode.OPPONENT_THROW_IN
    if play_mode == "KickIn_Right":
        return SoccerGameMode.OPPONENT_THROW_IN if left_side else SoccerGameMode.OWN_THROW_IN
    if play_mode == "corner_kick_left":
        return SoccerGameMode.OWN_CORNER_KICK if left_side else SoccerGameMode.OPPONENT_CORNER_KICK
    if play_mode == "corner_kick_right":
        return SoccerGameMode.OPPONENT_CORNER_KICK if left_side else SoccerGameMode.OWN_CORNER_KICK
    if play_mode == "goal_kick_left":
        return SoccerGameMode.OWN_GOAL_KICK if left_side else SoccerGameMode.OPPONENT_GOAL_KICK
    if play_mode == "goal_kick_right":
        return SoccerGameMode.OPPONENT_GOAL_KICK if left_side else SoccerGameMode.OWN_GOAL_KICK
    if play_mode == "offside_left":
        return SoccerGameMode.OWN_OFFSIDE if left_side else SoccerGameMode.OPPONENT_OFFSIDE
    if play_mode == "offside_right":
        return SoccerGameMode.OPPONENT_OFFSIDE if left_side else SoccerGameMode.OWN_OFFSIDE
    if play_mode == "GameOver":
        return SoccerGameMode.GAME_OVER
    if play_mode == "Goal_Left":
        return SoccerGameMode.OWN_GOAL if left_side else SoccerGameMode.OPPONENT_GOAL
    if play_mode == "Goal_Right":
        return SoccerGameMode.OPPONENT_GOAL if left_side else SoccerGameMode.OWN_GOAL
    if play_mode == "free_kick_left":
        return SoccerGameMode.OWN_FREE_KICK if left_side else SoccerGameMode.OPPONENT_FREE_KICK
    if play_mode == "free_kick_right":
        return SoccerGameMode.OPPONENT_FREE_KICK if left_side else SoccerGameMode.OWN_FREE_KICK
    if play_mode == "direct_free_kick_left":
        return SoccerGameMode.OWN_DIRECT_FREE_KICK if left_side else SoccerGameMode.OPPONENT_DIRECT_FREE_KICK
    if play_mode == "direct_free_kick_right":
        return SoccerGameMode.OPPONENT_DIRECT_FREE_KICK if left_side else SoccerGameMode.OWN_DIRECT_FREE_KICK
    if play_mode == "NONE":
        return SoccerGameMode.NONE
    if play_mode == "pass_left":
        return SoccerGameMode.OWN_PASS if left_side else SoccerGameMode.OPPONENT_PASS
    if play_mode == "pass_right":
        return SoccerGameMode.OPPONENT_PASS if left_side else SoccerGameMode.OWN_PASS
    if play_mode == "Freeze":
        return SoccerGameMode.FREEZE
    if play_mode == "penalty_kick_left":
        return SoccerGameMode.OWN_PENALTY_KICK if left_side else SoccerGameMode.OPPONENT_PENALTY_KICK
    if play_mode == "penalty_kick_right":
        return SoccerGameMode.OPPONENT_PENALTY_KICK if left_side else SoccerGameMode.OWN_PENALTY_KICK
    if play_mode == "penalty_shoot_left":
        return SoccerGameMode.OWN_PENALTY_SHOOT if left_side else SoccerGameMode.OPPONENT_PENALTY_SHOOT
    if play_mode == "penalty_shoot_right":
        return SoccerGameMode.OPPONENT_PENALTY_SHOOT if left_side else SoccerGameMode.OWN_PENALTY_SHOOT

    # print("WARNING: Unknown play mode: \"" + play_mode + "\"!")

    return SoccerGameMode.NONE


class PSoccerGameState(Protocol):
    """
    Protocol for a soccer game state.
    """

    def get_time(self) -> float:
        """
        Retrieve the time of the last update.
        """

    def get_play_time(self) -> float:
        """
        Retrieve the current play time.
        """

    def get_play_side(self) -> PlaySide:
        """
        Retrieve the current play side.
        """

    def get_game_mode(self) -> SoccerGameMode:
        """
        Retrieve the current game mode.
        """

    def get_own_score(self) -> int:
        """
        Retrieve the current score of our own team.
        """

    def get_opponent_score(self) -> int:
        """
        Retrieve the current score of the opponent team.
        """

    def is_game_running(self) -> bool:
        """
        Check if the game is currently running.
        """

    def is_own_kick(self) -> bool:
        """
        Check if our team has exclusive access to the ball and is expected to perform a kick.
        """

    def is_opponent_kick(self) -> bool:
        """
        Check if the opponent team has exclusive access to the ball and is expected to perform a kick.
        """

    def is_beaming_allowed(self) -> bool:
        """
        Check if beaming is currently allowed / enabled (although beaming is unfortunately still not well supported by real robots...).
        """

    def get_mode_time(self, mode: SoccerGameMode | None = None) -> float:
        """
        Retrieve the time at which the given game mode has last been set (0 when is has not been encountered in this game, yet).

        Note: If no mode is specified, the current game mode of this game state is used.
        """

    def get_play_side_time(self, play_side: PlaySide | None = None) -> float:
        """
        Retrieve the time at which the given play side has last been set (0 when is has not been encountered in this game, yet).

        Note: If no play side is specified, the current play side of this game state is used.
        """


class PMutableSoccerGameState(PSoccerGameState, PMutableModel, Protocol):
    """
    Protocol for a mutable soccer game state.
    """


class SoccerGameState:
    """
    Representation of a soccer game state.
    """

    _RUNNING_MODES = frozenset([
        SoccerGameMode.PLAY_ON,
        SoccerGameMode.OWN_KICK_OFF,
        SoccerGameMode.OPPONENT_KICK_OFF,
        SoccerGameMode.OWN_GOAL_KICK,
        SoccerGameMode.OPPONENT_GOAL_KICK,
        SoccerGameMode.OWN_FREE_KICK,
        SoccerGameMode.OPPONENT_FREE_KICK,
        SoccerGameMode.OWN_DIRECT_FREE_KICK,
        SoccerGameMode.OPPONENT_DIRECT_FREE_KICK,
        SoccerGameMode.OWN_THROW_IN,
        SoccerGameMode.OPPONENT_THROW_IN,
        SoccerGameMode.OWN_CORNER_KICK,
        SoccerGameMode.OPPONENT_CORNER_KICK,
        SoccerGameMode.OWN_PASS,
        SoccerGameMode.OPPONENT_PASS,
        SoccerGameMode.OWN_PENALTY_KICK,
        SoccerGameMode.OPPONENT_PENALTY_KICK,
        SoccerGameMode.OWN_PENALTY_SHOOT,
        SoccerGameMode.OPPONENT_PENALTY_SHOOT
    ])

    _BEAM_MODES = frozenset([
        SoccerGameMode.OWN_GOAL,
        SoccerGameMode.OPPONENT_GOAL,
        SoccerGameMode.BEFORE_KICK_OFF
    ])

    _OWN_KICK_MODES = frozenset([
        SoccerGameMode.OWN_CORNER_KICK,
        SoccerGameMode.OWN_FREE_KICK,
        SoccerGameMode.OWN_DIRECT_FREE_KICK,
        SoccerGameMode.OWN_GOAL_KICK,
        SoccerGameMode.OWN_THROW_IN,
        SoccerGameMode.OWN_KICK_OFF,
        SoccerGameMode.OWN_PASS,
        SoccerGameMode.OWN_PENALTY_KICK,
        SoccerGameMode.OWN_PENALTY_SHOOT
    ])

    _OPPONENT_KICK_MODES = frozenset([
        SoccerGameMode.OPPONENT_CORNER_KICK,
        SoccerGameMode.OPPONENT_FREE_KICK,
        SoccerGameMode.OPPONENT_DIRECT_FREE_KICK,
        SoccerGameMode.OPPONENT_GOAL_KICK,
        SoccerGameMode.OPPONENT_THROW_IN,
        SoccerGameMode.OPPONENT_KICK_OFF,
        SoccerGameMode.OPPONENT_PASS,
        SoccerGameMode.OPPONENT_PENALTY_KICK,
        SoccerGameMode.OPPONENT_PENALTY_SHOOT
    ])

    def __init__(self, team_name: str) -> None:
        """
        Construct a new soccer game state.
        """

        self._time: float = 0.0
        self._own_team_name: str = team_name
        self._opponent_team_name: str = ""
        self._play_time: float = 0.0
        self._game_mode: SoccerGameMode = SoccerGameMode.BEFORE_KICK_OFF
        self._play_side: PlaySide = PlaySide.LEFT
        self._own_score: int = 0
        self._opponent_score: int = 0

        self._game_mode_times: dict[SoccerGameMode, float] = {gm: 0.0 for gm in SoccerGameMode}
        self._play_side_times: dict[PlaySide, float] = {ps: 0.0 for ps in PlaySide}

    def get_time(self) -> float:
        """
        Retrieve the time of the last update.
        """

        return self._time

    def get_own_team_name(self) -> str:
        """
        Retrieve the name of the own team.
        """

        return self._own_team_name

    def get_opponent_team_name(self) -> str:
        """
        Retrieve the name of the opponent team.
        """

        return self._opponent_team_name

    def get_play_time(self) -> float:
        """
        Retrieve the current play time.
        """

        return self._play_time

    def get_play_side(self) -> PlaySide:
        """
        Retrieve the current play side.
        """

        return self._play_side

    def get_game_mode(self) -> SoccerGameMode:
        """
        Retrieve the current game mode.
        """

        return self._game_mode

    def get_own_score(self) -> int:
        """
        Retrieve the current score of our own team.
        """

        return self._own_score

    def get_opponent_score(self) -> int:
        """
        Retrieve the current score of the opponent team.
        """

        return self._opponent_score

    def is_game_running(self) -> bool:
        """
        Check if the game is currently running.
        """

        return self._game_mode in SoccerGameState._RUNNING_MODES

    def is_own_kick(self) -> bool:
        """
        Check if our team has exclusive access to the ball and is expected to perform a kick.
        """

        return self._game_mode in SoccerGameState._OWN_KICK_MODES

    def is_opponent_kick(self) -> bool:
        """
        Check if the opponent team has exclusive access to the ball and is expected to perform a kick.
        """

        return self._game_mode in SoccerGameState._OPPONENT_KICK_MODES

    def is_beaming_allowed(self) -> bool:
        """
        Check if beaming is currently allowed / enabled (although beaming is unfortunately still not well supported by real robots...).
        """

        return self._game_mode in SoccerGameState._BEAM_MODES

    def get_mode_time(self, mode: SoccerGameMode | None = None) -> float:
        """
        Retrieve the time at which the given game mode has last been set (0 when is has not been encountered in this game, yet).

        Note: If no mode is specified, the current game mode of this game state is used.
        """

        return self._game_mode_times[self._game_mode if mode is None else mode]

    def get_play_side_time(self, play_side: PlaySide | None = None) -> float:
        """
        Retrieve the time at which the given play side has last been set (0 when is has not been encountered in this game, yet).

        Note: If no play side is specified, the current play side of this game state is used.
        """

        return self._play_side_times[self._play_side if play_side is None else play_side]

    def update(self, perception: Perception) -> None:
        """
        Update the state of the game state from the given perceptions.
        """

        # fetch game state perceptor
        perceptor = perception.get_perceptor("game_state", SoccerGameStatePerceptor)
        if perceptor is None:
            return

        # update state
        self._time = perception.get_time()
        self._play_time = perceptor.play_time

        perceived_play_side = PlaySide.from_value(perceptor.play_side)
        if perceived_play_side not in {PlaySide.UNKNOWN, self._play_side}:
            self._play_side = perceived_play_side
            self._play_side_times[self._play_side] = self._time

        perceived_game_mode = decode_rcss_game_mode(perceptor.play_mode, self._play_side)
        if perceived_game_mode != self._game_mode:
            self._game_mode = perceived_game_mode
            self._game_mode_times[self._game_mode] = self._time

        self._own_score = perceptor.score_left if self._play_side == PlaySide.LEFT else perceptor.score_right
        self._opponent_score = perceptor.score_right if self._play_side == PlaySide.LEFT else perceptor.score_left
