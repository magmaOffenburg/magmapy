from math import pi
from typing import Final

from magma.agent.model.robot.robot_model import PRobotModel
from magma.agent.model.robot.sensors import Loc3DSensor
from magma.agent.model.world.objects import InformationSource
from magma.common.math.geometry.pose import P3D_ZERO
from magma.common.math.geometry.rotation import R3D_IDENTITY, axis_angle
from magma.common.math.geometry.vector import V3D_UNIT_Z, V3D_ZERO
from magma.rcss.model.robot.rcss_sensors import RCSSVisionSensor
from magma.soccer_agent.model.game_state import PlaySide, PSoccerGameState
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_objects import SoccerPlayer
from magma.soccer_agent.model.world.soccer_world import SoccerWorld

PLAYER_REMEMBRANCE_TIME: Final[float] = 10.0
"""The time (in seconds) how long we remember a player detection."""


class RCSSSMJSoccerWorld(SoccerWorld):
    """Model representing a RoboCup Soccer Simulation MuJoCo soccer world."""

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

        super().__init__(team_name, player_no, field_desc, ball_radius)

    def _localize(self, robot: PRobotModel, game_state: PSoccerGameState) -> bool:
        """Localize robot."""

        # try localizing via global positioning system (external localizer)
        gps = robot.get_sensor('torso_loc', Loc3DSensor)
        if gps is not None and gps.received_update():
            pos = gps.get_location().pos
            rot = gps.get_location().rot

            if game_state.play_side == PlaySide.RIGHT:
                # mirror location if playing from right to left
                mirror_rot = axis_angle(V3D_UNIT_Z, pi)
                pos = mirror_rot.tf_vec(pos)
                rot = mirror_rot.tf_rot(rot)

            self._this_player.update_location(gps.get_time(), pos, rot)
            return True

        return False

    def _update_players(self, robot: PRobotModel, game_state: PSoccerGameState) -> bool:
        # fetch vision sensor
        cam = robot.get_sensor('vision', RCSSVisionSensor)
        if cam is None or not cam.received_update():
            return False

        # reset visibility of known players
        player: SoccerPlayer | None = None
        for player in self._known_players.values():
            player.reset_visibility()

        # fetch camera pose
        cam_body = robot.get_body(cam.frame_id)
        cam_pose = P3D_ZERO if cam_body is None else cam_body.get_pose()

        for player_detection in cam.get_player_detections():
            if not player_detection.team_name or player_detection.player_no < 0:
                # skip incomplete player detections
                continue

            n_body_parts = len(player_detection.body_parts)
            if n_body_parts < 1:
                # skip empty player detections
                continue

            own_team = self._this_player.team_name == player_detection.team_name
            if own_team and player_detection.player_no == self._this_player.player_no:
                # skip self detections
                continue

            # try fetch existing player instance for player detection
            player_id = f'{player_detection.team_name}-{player_detection.player_no}'
            player = self._known_players.get(player_id, None)

            # create new player instance in case no matching player exists
            if player is None:
                player = SoccerPlayer(player_detection.team_name, player_detection.player_no, own_team=own_team, is_goalie=False)
                self._known_players[player_id] = player

            # calculate average position of detected body parts
            seen_pos = V3D_ZERO
            for _, pos in player_detection.body_parts:
                seen_pos += pos

            # update player information
            seen_pos = seen_pos / n_body_parts
            local_pos = cam_pose.tf_vec(seen_pos)
            global_pos = self._this_player.get_pose().tf_vec(local_pos)
            player.update(cam.get_time(), InformationSource.VISION, global_pos, R3D_IDENTITY, V3D_ZERO)

        # extract valid players list
        self._players = [player for player in self._known_players.values() if player.get_age(self._time) < PLAYER_REMEMBRANCE_TIME]

        # FIXME: decide how to handle visibility flag of a soccer player (at the moment, an object only keeps visible, if it keeps being detected in every vision cycle)
        # # extract valid players list and reset visibility of others
        # self._players.clear()
        # for player in self._known_players.values():
        #     if player.get_age(self._time) > PLAYER_REMEMBRANCE_TIME:
        #         player.reset_visibility()
        #     else:
        #         self._players.append(player)

        return True
