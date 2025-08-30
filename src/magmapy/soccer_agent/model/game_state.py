from __future__ import annotations

from enum import Enum
from typing import Protocol


class PlaySide(Enum):
    """Enum specifying the different play side options in a soccer game,"""

    UNKNOWN = 'unknown'
    """We play from left to right."""

    LEFT = 'left'
    """We play from left to right."""

    RIGHT = 'right'
    """We play from right to left."""

    @staticmethod
    def from_value(side_id: str) -> PlaySide:
        """Fetch the enum entry corresponding to the given side identifier.

        Parameter
        ---------
        side_id : str
            The side identifier.
        """

        side_id = side_id.lower()

        for v in PlaySide:
            if v.value == side_id:
                return v

        # print("WARNING: Unknown Play Side: \"" + side_id + "\"!")

        return PlaySide.UNKNOWN


class PlayMode(Enum):
    """Enum specifying the different play modes of a soccer game."""

    NONE = 'none'
    """No game mode or an unknown one (should not be used!)."""

    TIMEOUT = 'timeout'
    """Some timeout situation for a team or the referees.

    The game is on hold and nobody should actively move around.
    """

    BEFORE_KICK_OFF = 'before-kick-off'
    """The game has not started yet."""

    GAME_OVER = 'game-over'
    """The game is over."""

    OWN_KICK_OFF = 'own-kick-off'
    """Kick-off for our team.

    The ball is in the center and our team is allowed to kick it first.
    """

    OPPONENT_KICK_OFF = 'opponent-kick-off'
    """Kick-off for the opponent team.

    The ball is in the center and the opponent team is allowed to kick it first.
    """

    PLAY_ON = 'play-on'
    """Normal gameplay.

    The game is processing normally, no special rules are in place.
    """

    OWN_GOAL_KICK = 'own-goal-kick'
    """Goal-kick for our team.

    The opponent team kicked the ball outside the play field across our side line and our team is allowed to perform a goal kick (kick-off from goal).
    """

    OPPONENT_GOAL_KICK = 'opponent-goal-kick'
    """Goal-kick for the opponent team.

    Our team kicked the ball outside the play field across the opponent side line and the opponent team is allowed to perform a goal kick (kick-off from goal).
    """

    OWN_THROW_IN = 'own-throw-in'
    """Throw-in for our team.

    The opponent team has kicked the ball outside the play field across the upper / lower ground line and our team is allowed to throw / kick it back into the field.
    """

    OPPONENT_THROW_IN = 'opponent-throw-in'
    """Throw-in for the opponent team.

    Our team has kicked the ball outside the play field across the upper / lower ground line and the opponent team is allowed to throw / kick it back into the field.
    """

    OWN_CORNER_KICK = 'own-corner-kick'
    """Corner-kick for our team.

    The opponent team kicked the ball outside the play field across their side line and our team is allowed to perform a corner kick.
    """

    OPPONENT_CORNER_KICK = 'opponent-corner-kick'
    """Corner-kick for the opponent team.

    Our team kicked the ball outside the play field across our side line and the opponent team is allowed to perform a corner kick.
    """

    OWN_FREE_KICK = 'own-free-kick'
    """Indirect free-kick for our team.

    Our team got an indirect free kick and may kick the ball first.
    """

    OPPONENT_FREE_KICK = 'opponent-free-kick'
    """Indirect free-kick for the opponent team.

    The opponent team got an indirect free kick and may kick the ball first.
    """

    OWN_DIRECT_FREE_KICK = 'own-direct-free-kick'
    """Direct free-kick for our team.

    Our team got a direct free kick and may kick the ball first.
    """

    OPPONENT_DIRECT_FREE_KICK = 'opponent-direct-free-kick'
    """Direct free-kick for the opponent team.

    The opponent team got a direct free kick and may kick the ball first.
    """

    OWN_PENALTY_KICK = 'own-penalty-kick'
    """Penalty-kick for our team.

    Our team should perform a penalty kick. The ball is at the penalty spot in front of the opponent goal.
    """

    OPPONENT_PENALTY_KICK = 'opponent-penalty-kick'
    """Penalty-kick for the opponent team.

    The opponent team should perform a penalty kick. The ball is at the penalty spot in front of our goal.
    """

    OWN_PENALTY_SHOOT = 'own-penalty-shoot'
    """Penalty-shoot for our team.

    Our team should perform a penalty shootout by somehow dribbling / kicking the ball into the opponent goal. The ball is initially at the center of the field.
    """

    OPPONENT_PENALTY_SHOOT = 'opponent-penalty-shoot'
    """Penalty-shoot for the opponent team.

    The opponent team should perform a penalty shootout by somehow dribbling / kicking the ball into our goal. The ball is initially at the center of the field.
    """


class PlayModePhase(Enum):
    """Enum specifying the different phases of a play mode."""

    FREEZE = 'freeze'
    """Freeze / don't move."""

    PREPARATION = 'preparation'
    """The preparation phase. During this phase, players should prepare themselves for the current play mode."""

    SET = 'set'
    """The set game phase. During this phase, the game is setup for the current play mode (e.g. the ball is placed, misplaced players are removed, etc.)."""

    RUNNING = 'running'
    """The normal game phase."""


class PSoccerGameState(Protocol):
    """Protocol for a soccer game state."""

    @property
    def time(self) -> float:
        """The time of the last update."""

    @property
    def own_team_name(self) -> str:
        """The name of the own team."""

    @property
    def opponent_team_name(self) -> str:
        """The name of the opponent team."""

    @property
    def play_time(self) -> float:
        """The current play time."""

    @property
    def play_side(self) -> PlaySide:
        """The current play side."""

    @property
    def play_mode(self) -> PlayMode:
        """The current play mode."""

    @property
    def play_mode_phase(self) -> PlayModePhase:
        """The current play mode phase."""

    @property
    def own_score(self) -> int:
        """The current score of our own team."""

    @property
    def opponent_score(self) -> int:
        """The current score of the opponent team."""

    def is_game_running(self) -> bool:
        """Check if the game is currently running."""

    def is_own_kick(self) -> bool:
        """Check if our team has exclusive access to the ball and is expected to perform a kick."""

    def is_opponent_kick(self) -> bool:
        """Check if the opponent team has exclusive access to the ball and is expected to perform a kick."""

    def get_play_mode_time(self, mode: PlayMode | None = None) -> float:
        """Retrieve the time at which the given play mode has last been set (0 when is has not been encountered in this game, yet).

        Note: If no mode is specified, the current play mode of this game state is used.

        Parameter
        ---------
        mode : PlayMode | None, default=None
            The soccer play mode for which to fetch the last activation time. If ``None``, the current play mode is used.
        """

    def get_play_mode_phase_time(self, phase: PlayModePhase | None = None) -> float:
        """Retrieve the time at which the given game phase has last been set (0 when is has not been encountered in this game, yet).

        Note: If no phase is specified, the current game phase of this game state is used.

        Parameter
        ---------
        phase : PlayModePhase | None, default=None
            The soccer play mode phase for which to fetch the last activation time. If ``None``, the current play mode phase is used.
        """

    def get_play_side_time(self, play_side: PlaySide | None = None) -> float:
        """Retrieve the time at which the given play side has last been set (0 when is has not been encountered in this game, yet).

        Note: If no play side is specified, the current play side of this game state is used.

        Parameter
        ---------
        play_side: PlaySide | None, default=None
            The play side for which to fetch the last activation time. If ``None``, the current play side is used.
        """


class SoccerGameState:
    """Representation of a soccer game state."""

    _RUNNING_MODES = frozenset(
        [
            PlayMode.PLAY_ON,
            PlayMode.OWN_KICK_OFF,
            PlayMode.OPPONENT_KICK_OFF,
            PlayMode.OWN_GOAL_KICK,
            PlayMode.OPPONENT_GOAL_KICK,
            PlayMode.OWN_FREE_KICK,
            PlayMode.OPPONENT_FREE_KICK,
            PlayMode.OWN_DIRECT_FREE_KICK,
            PlayMode.OPPONENT_DIRECT_FREE_KICK,
            PlayMode.OWN_THROW_IN,
            PlayMode.OPPONENT_THROW_IN,
            PlayMode.OWN_CORNER_KICK,
            PlayMode.OPPONENT_CORNER_KICK,
            PlayMode.OWN_PENALTY_KICK,
            PlayMode.OPPONENT_PENALTY_KICK,
            PlayMode.OWN_PENALTY_SHOOT,
            PlayMode.OPPONENT_PENALTY_SHOOT,
        ]
    )

    _OWN_KICK_MODES = frozenset(
        [
            PlayMode.OWN_CORNER_KICK,
            PlayMode.OWN_FREE_KICK,
            PlayMode.OWN_DIRECT_FREE_KICK,
            PlayMode.OWN_GOAL_KICK,
            PlayMode.OWN_THROW_IN,
            PlayMode.OWN_KICK_OFF,
            PlayMode.OWN_PENALTY_KICK,
            PlayMode.OWN_PENALTY_SHOOT,
        ]
    )

    _OPPONENT_KICK_MODES = frozenset(
        [
            PlayMode.OPPONENT_CORNER_KICK,
            PlayMode.OPPONENT_FREE_KICK,
            PlayMode.OPPONENT_DIRECT_FREE_KICK,
            PlayMode.OPPONENT_GOAL_KICK,
            PlayMode.OPPONENT_THROW_IN,
            PlayMode.OPPONENT_KICK_OFF,
            PlayMode.OPPONENT_PENALTY_KICK,
            PlayMode.OPPONENT_PENALTY_SHOOT,
        ]
    )

    def __init__(self, team_name: str) -> None:
        """Construct a new soccer game state.

        Parameter
        ---------
        team_name : str
            Our team name.
        """

        self._time: float = 0.0
        """The time of the most recent update."""

        self._own_team_name: str = team_name
        """The name of our team."""

        self._opponent_team_name: str = ''
        """The name of the opponent team."""

        self._play_time: float = 0.0
        """The current play time."""

        self._game_mode: PlayMode = PlayMode.BEFORE_KICK_OFF
        """The current game mode."""

        self._game_phase: PlayModePhase = PlayModePhase.FREEZE
        """The current game phase."""

        self._play_side: PlaySide = PlaySide.LEFT
        """The current play side of our team."""

        self._own_score: int = 0
        """The score of our team."""

        self._opponent_score: int = 0
        """The score of the opponent team."""

        self._play_mode_times: dict[PlayMode, float] = {pm: 0.0 for pm in PlayMode}
        """History of play mode changes."""

        self._play_mode_phase_times: dict[PlayModePhase, float] = {pmp: 0.0 for pmp in PlayModePhase}
        """History of play mode phase changes."""

        self._play_side_times: dict[PlaySide, float] = {ps: 0.0 for ps in PlaySide}
        """History of play side changes."""

    @property
    def time(self) -> float:
        """Retrieve the time of the last update."""

        return self._time

    @property
    def own_team_name(self) -> str:
        """The name of the own team."""

        return self._own_team_name

    @property
    def opponent_team_name(self) -> str:
        """The name of the opponent team."""

        return self._opponent_team_name

    @property
    def play_time(self) -> float:
        """The current play time."""

        return self._play_time

    @property
    def play_side(self) -> PlaySide:
        """The current play side."""

        return self._play_side

    @property
    def play_mode(self) -> PlayMode:
        """The current play mode."""

        return self._game_mode

    @property
    def play_mode_phase(self) -> PlayModePhase:
        """The current play mode phase."""

        return self._game_phase

    @property
    def own_score(self) -> int:
        """The current score of our own team."""

        return self._own_score

    @property
    def opponent_score(self) -> int:
        """The current score of the opponent team."""

        return self._opponent_score

    def is_game_running(self) -> bool:
        """Check if the game is currently running."""

        return self._game_mode in SoccerGameState._RUNNING_MODES

    def is_own_kick(self) -> bool:
        """Check if our team has exclusive access to the ball and is expected to perform a kick."""

        return self._game_mode in SoccerGameState._OWN_KICK_MODES

    def is_opponent_kick(self) -> bool:
        """Check if the opponent team has exclusive access to the ball and is expected to perform a kick."""

        return self._game_mode in SoccerGameState._OPPONENT_KICK_MODES

    def get_play_mode_time(self, mode: PlayMode | None = None) -> float:
        """Retrieve the time at which the given play mode has last been set (0 when is has not been encountered in this game, yet).

        Note: If no mode is specified, the current play mode of this game state is used.

        Parameter
        ---------
        mode : PlayMode | None, default=None
            The soccer play mode for which to fetch the last activation time. If ``None``, the current play mode is used.
        """

        return self._play_mode_times[self._game_mode if mode is None else mode]

    def get_play_mode_phase_time(self, phase: PlayModePhase | None = None) -> float:
        """Retrieve the time at which the given game phase has last been set (0 when is has not been encountered in this game, yet).

        Note: If no phase is specified, the current game phase of this game state is used.

        Parameter
        ---------
        phase : PlayModePhase | None, default=None
            The soccer play mode phase for which to fetch the last activation time. If ``None``, the current play mode phase is used.
        """

        return self._play_mode_phase_times[self._game_phase if phase is None else phase]

    def get_play_side_time(self, play_side: PlaySide | None = None) -> float:
        """Retrieve the time at which the given play side has last been set (0 when is has not been encountered in this game, yet).

        Note: If no play side is specified, the current play side of this game state is used.

        Parameter
        ---------
        play_side: PlaySide | None, default=None
            The play side for which to fetch the last activation time. If ``None``, the current play side is used.
        """

        return self._play_side_times[self._play_side if play_side is None else play_side]

    def update(
        self,
        time: float,
        play_time: float,
        *,
        opponent_team_name: str | None = None,
        play_side: PlaySide | None = None,
        play_mode: PlayMode | None = None,
        play_mode_phase: PlayModePhase | None = None,
        own_score: int | None = None,
        opponent_score: int | None = None,
    ) -> None:
        """Update the state of the game state from the given perceptions.

        Parameter
        ---------
        time: float
            The current time.

        play_time: float
            The current play time.

        opponent_team_name: str | None, default=None
            The name of the opponent team.

        play_side: PlaySide | None, default=None
            The current play side of our team.

        play_mode: SoccerGameMode | None, default=None
            The current play mode.

        play_mode_phase: SoccerGamePhase | None, default=None
            The current play mode phase.

        own_score: int | None, default=None
            The score of our team.

        opponent_score: int | None, default=None
            The score of the opponent team.
        """

        self._time = time
        self._play_time = play_time

        if opponent_team_name is not None:
            self._opponent_team_name = opponent_team_name

        if play_side is not None and play_side != self._play_side:
            self._play_side = play_side
            self._play_side_times[self._play_side] = self._time

        if play_mode is not None and play_mode != self._game_mode:
            self._game_mode = play_mode
            self._play_mode_times[self._game_mode] = self._time

        if play_mode_phase is not None and play_mode_phase != self._game_phase:
            self._game_phase = play_mode_phase
            self._play_mode_phase_times[self._game_phase] = self._time

        if own_score is not None:
            self._own_score = own_score

        if opponent_score is not None:
            self._opponent_score = opponent_score
