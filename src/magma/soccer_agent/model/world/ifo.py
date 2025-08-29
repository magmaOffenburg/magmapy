from collections.abc import Sequence
from typing import Protocol

from magma.soccer_agent.model.world.soccer_objects import PSoccerBall, PSoccerPlayer


class PSoccerIFO(Protocol):
    """Protocol for soccer related indexical functional object collections."""

    @property
    def active_players(self) -> Sequence[PSoccerPlayer]:
        """The list of active / capable players (excluding this-player)."""

    @property
    def active_teammates(self) -> Sequence[PSoccerPlayer]:
        """The list of active / capable team mates (excluding this-player)."""

    @property
    def active_opponents(self) -> Sequence[PSoccerPlayer]:
        """The list of active / capable opponent players."""

    @property
    def own_goalie(self) -> PSoccerPlayer | None:
        """The goalie player of our team."""

    @property
    def opponent_goalie(self) -> PSoccerPlayer | None:
        """The goalie player of our team."""

    @property
    def players_at_ball(self) -> Sequence[PSoccerPlayer]:
        """The list of active players sorted by their distance to the ball (including this-player if capable)."""

    @property
    def own_players_at_ball(self) -> Sequence[PSoccerPlayer]:
        """The list of active own players sorted by their distance to the ball (including this-player if capable)."""

    @property
    def opponent_players_at_ball(self) -> Sequence[PSoccerPlayer]:
        """The list of active opponent players sorted by their distance to the ball."""

    @property
    def players_at_me(self) -> Sequence[PSoccerPlayer]:
        """The list of active players sorted by their distance to myself."""

    @property
    def teammates_at_me(self) -> Sequence[PSoccerPlayer]:
        """The list of active team mates sorted by their distance to myself."""

    @property
    def opponents_at_me(self) -> Sequence[PSoccerPlayer]:
        """The list of active opponent players sorted by their distance to myself."""

    def get_own_player_at_ball(self) -> PSoccerPlayer | None:
        """Return the closest own player to the ball."""

    def get_opponent_player_at_ball(self) -> PSoccerPlayer | None:
        """Return the closest opponent player to the ball."""

    def get_teammate_at_me(self) -> PSoccerPlayer | None:
        """Return the closest team mate to myself."""

    def get_opponent_at_me(self) -> PSoccerPlayer | None:
        """Return the closest opponent player to myself."""


class SoccerIFO:
    """Collection of soccer related indexical functional objects."""

    def __init__(self) -> None:
        """Construct a new IFO calculator."""

        self.active_players: list[PSoccerPlayer] = []
        """The list of active / capable players (excluding this-player)."""

        self.active_teammates: list[PSoccerPlayer] = []
        """The list of active / capable team mates (excluding this-player)."""

        self.active_opponents: list[PSoccerPlayer] = []
        """The list of active / capable opponent players."""

        self.own_goalie: PSoccerPlayer | None = None
        """The goalie player of our team."""

        self.opponent_goalie: PSoccerPlayer | None = None
        """The goalie player of the opponent team."""

        self.players_at_ball: list[PSoccerPlayer] = []
        """The list of active players sorted by their distance to the ball (including this-player if capable)."""

        self.own_players_at_ball: list[PSoccerPlayer] = []
        """The list of active own players sorted by their distance to the ball (including this-player if capable)."""

        self.opponent_players_at_ball: list[PSoccerPlayer] = []
        """The list of active opponent players sorted by their distance to the ball."""

        self.players_at_me: list[PSoccerPlayer] = []
        """The list of active players sorted by their distance to myself."""

        self.teammates_at_me: list[PSoccerPlayer] = []
        """The list of active team mates sorted by their distance to myself."""

        self.opponents_at_me: list[PSoccerPlayer] = []
        """The list of active opponent players sorted by their distance to myself."""

    def get_own_player_at_ball(self) -> PSoccerPlayer | None:
        """Return the closest own player to the ball (including this-player if capable)."""

        return self.own_players_at_ball[0] if self.own_players_at_ball else None

    def get_opponent_player_at_ball(self) -> PSoccerPlayer | None:
        """Return the closest opponent player to the ball."""

        return self.opponent_players_at_ball[0] if self.opponent_players_at_ball else None

    def get_teammate_at_me(self) -> PSoccerPlayer | None:
        """Return the closest team mate to myself."""

        return self.teammates_at_me[0] if self.teammates_at_me else None

    def get_opponent_at_me(self) -> PSoccerPlayer | None:
        """Return the closest opponent player to myself."""

        return self.opponents_at_me[0] if self.opponents_at_me else None

    def update(self, players: Sequence[PSoccerPlayer], ball: PSoccerBall, this_player: PSoccerPlayer) -> None:
        """Update the state of the model."""

        # filter active players (excluding this-player)
        self.active_players = [player for player in players if not player.incapable()]
        self.active_teammates = [player for player in self.active_players if player.own_team]
        self.active_opponents = [player for player in self.active_players if not player.own_team]

        # calculate players at ball (including this-player if capable)
        players_at_obj = [(player, player.distance_to_2d(ball)) for player in self.active_players]
        if not this_player.incapable():
            players_at_obj.append((this_player, this_player.distance_to_2d(ball)))
        players_at_obj.sort(key=lambda entry: entry[1])

        self.players_at_ball = [entry[0] for entry in players_at_obj]
        self.own_players_at_ball = [player for player in self.players_at_ball if player.own_team]
        self.opponent_players_at_ball = [player for player in self.players_at_ball if not player.own_team]

        # calculate players at me
        players_at_obj = [(player, player.distance_to_2d(this_player)) for player in self.active_players]
        players_at_obj.sort(key=lambda entry: entry[1])

        self.players_at_me = [entry[0] for entry in players_at_obj]
        self.teammates_at_me = [player for player in self.players_at_me if player.own_team]
        self.opponents_at_me = [player for player in self.players_at_me if not player.own_team]

        # fetch own goalie player
        self.own_goalie = None
        for player in self.own_players_at_ball:
            if player.is_goalie():
                self.own_goalie = player
                break

        # fetch opponent goalie player
        self.opponent_goalie = None
        for player in self.opponent_players_at_ball:
            if player.is_goalie():
                self.opponent_goalie = player
                break
