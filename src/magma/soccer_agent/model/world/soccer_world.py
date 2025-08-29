from collections.abc import Sequence
from typing import Protocol

from magma.agent.communication.perception import Perception
from magma.agent.model.robot.robot_model import PRobotModel
from magma.agent.model.robot.sensors import Loc3DSensor, VisionSensor
from magma.agent.model.world.objects import InformationSource, LineLandmark, PointLandmark
from magma.common.math.geometry.pose import P3D_ZERO
from magma.common.math.geometry.rotation import R3D_IDENTITY
from magma.common.math.geometry.vector import V3D_ZERO
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

    def update(self, perception: Perception, robot: PRobotModel) -> None:
        """Update the state of the model from the given perceptions.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.

        robot : PRobotModel
            The robot model.
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

    def update(self, perception: Perception, robot: PRobotModel) -> None:
        """Update the state of the world model from the given perceptions."""

        self._time = perception.get_time()

        self._localize(robot)

        self._update_ball(robot)

    def _localize(self, robot: PRobotModel) -> bool:
        """Localize robot."""

        # try localizing via global positioning system (external localizer)
        gps = robot.get_sensor('torso_loc', Loc3DSensor)
        if gps is not None and gps.received_update():
            loc = gps.get_location()
            self._this_player.update_location(gps.get_time(), loc.pos, loc.rot)
            return True

        return False

    def _update_ball(self, robot: PRobotModel) -> bool:
        """Update the ball information."""

        # fetch vision sensor
        cam = robot.get_sensor('vision', VisionSensor)
        if cam is None or not cam.received_update():
            return False

        # reset visibility of ball
        self._ball.reset_visibility()

        # fetch ball detections
        ball_detections = [obj for obj in cam.get_object_detections() if obj.name == 'B']
        if not ball_detections:
            return False

        # fetch camera pose
        cam_body = robot.get_body(cam.frame_id)
        cam_pose = P3D_ZERO if cam_body is None else cam_body.get_pose()

        # filter ball position and update ball object
        seen_pos = ball_detections[0].position
        local_pos = cam_pose.tf_vec(seen_pos)
        global_pos = self._this_player.get_pose().tf_vec(local_pos)
        # TODO: filter global ball position
        self._ball.update(cam.get_time(), InformationSource.VISION, global_pos, R3D_IDENTITY, V3D_ZERO)

        return True
