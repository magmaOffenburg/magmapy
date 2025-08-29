from collections.abc import Sequence
from typing import Protocol

from magma.agent.communication.perception import Loc3DPerceptor, Perception, Pos3DPerceptor, Rot3DPerceptor
from magma.agent.model.world.objects import LineLandmark, PointLandmark
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_map import PSoccerMap, SoccerMap
from magma.soccer_agent.model.world.soccer_objects import (
    PSoccerBall,
    PSoccerPlayer,
    PThisSoccerPlayer,
    SoccerBall,
    SoccerPlayer,
    ThisSoccerPlayer,
)


class PSoccerWorld(Protocol):
    """Soccer domain specific robot model."""

    def get_time(self) -> float:
        """Retrieve the time of the last update."""

    def get_point_landmarks(self) -> Sequence[PointLandmark]:
        """Retrieve the collection of known point landmarks."""

    def get_line_landmarks(self) -> Sequence[LineLandmark]:
        """Retrieve the collection of known line landmarks."""

    def get_ball(self) -> PSoccerBall:
        """Retrieve the soccer ball representation."""

    def get_this_player(self) -> PThisSoccerPlayer:
        """Retrieve this agent's representation in the world."""

    def get_players(self) -> Sequence[PSoccerPlayer]:
        """Retrieve the collection of soccer player representations within the world (excluding the this-player)."""

    def get_map_version(self) -> str:
        """Retrieve the soccer map version."""

    def get_map(self) -> PSoccerMap:
        """Retrieve the soccer map."""


class PMutableSoccerWorld(PSoccerWorld, Protocol):
    """Soccer domain specific robot model."""

    def update(self, perception: Perception) -> None:
        """Update the state of the model from the given perceptions.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """


class SoccerWorld:
    """Model representing a soccer world."""

    def __init__(
        self,
        team_name: str,
        player_no: int,
        field_desc: PSoccerFieldDescription,
        ball_radius: float,
    ) -> None:
        """Construct a new soccer world.

        Parameter
        ---------
        team_name : str
            The name of our team.

        player_no : int
            Our player number.

        field_desc : PSoccerFieldDescription
            The soccer field description.

        ball_radius : float
            The radius of the soccer ball.
        """

        # self._field_desc: PSoccerFieldDescription = field_desc

        self._time: float = 0.0

        # world objects
        self._point_landmarks: tuple[PointLandmark, ...] = tuple(PointLandmark(f.name, f.get_type(), f.get_known_position()) for f in field_desc.get_point_features())
        self._line_landmarks: tuple[LineLandmark, ...] = tuple(LineLandmark(f.name, f.get_type(), f.get_known_position1(), f.get_known_position2()) for f in field_desc.get_line_features())
        self._ball: SoccerBall = SoccerBall(ball_radius)
        self._this_player: ThisSoccerPlayer = ThisSoccerPlayer(team_name, player_no)
        self._players: tuple[SoccerPlayer, ...] = ()

        # map
        self._map_version: str = field_desc.__class__.__name__
        self._map: SoccerMap = SoccerMap(
            field_desc.get_field_dimensions(),
            field_desc.get_goal_dimensions(),
            field_desc.get_goalie_area_dimensions(),
            field_desc.get_penalty_area_dimensions(),
            field_desc.get_middle_circle_radius(),
            field_desc.get_penalty_spot_distance(),
            self._point_landmarks,
            self._line_landmarks,
        )

    def get_time(self) -> float:
        """Retrieve the time of the last update."""

        return self._time

    def get_point_landmarks(self) -> Sequence[PointLandmark]:
        """Retrieve the collection of known point landmarks."""

        return self._point_landmarks

    def get_line_landmarks(self) -> Sequence[LineLandmark]:
        """Retrieve the collection of known line landmarks."""

        return self._line_landmarks

    def get_ball(self) -> SoccerBall:
        """Retrieve the soccer ball representation."""

        return self._ball

    def get_this_player(self) -> ThisSoccerPlayer:
        """Retrieve this agent's representation in the world."""

        return self._this_player

    def get_players(self) -> Sequence[SoccerPlayer]:
        """Retrieve the collection of soccer player representations within the world (excluding the this-player)."""

        return self._players

    def get_map_version(self) -> str:
        """Retrieve the soccer map version."""

        return self._map_version

    def get_map(self) -> PSoccerMap:
        """Retrieve the soccer map."""

        return self._map

    def update(self, perception: Perception) -> None:
        """Update the state of the world model from the given perceptions."""

        self._time = perception.get_time()

        # try updating robot location
        loc_perceptor = perception.get_perceptor('torso_loc', Loc3DPerceptor)
        pos_perceptor = perception.get_perceptor('torso_pos', Pos3DPerceptor)
        rot_perceptor = perception.get_perceptor('torso_quat', Rot3DPerceptor)

        if loc_perceptor is not None:
            self._this_player.update_location(self._time, loc_perceptor.loc.pos, loc_perceptor.loc.rot)
        elif pos_perceptor is not None and rot_perceptor is not None:
            self._this_player.update_location(self._time, pos_perceptor.pos, rot_perceptor.rot)
        elif pos_perceptor is not None:
            self._this_player.update_location(self._time, pos_perceptor.pos, self._this_player.get_orientation())
        elif rot_perceptor is not None:
            self._this_player.update_location(self._time, self._this_player.get_position(), rot_perceptor.rot)

        # TODO: update objects
