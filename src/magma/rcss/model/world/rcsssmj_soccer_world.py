from math import pi

from magma.agent.model.robot.robot_model import PRobotModel
from magma.agent.model.robot.sensors import Loc3DSensor
from magma.common.math.geometry.rotation import axis_angle
from magma.common.math.geometry.vector import V3D_UNIT_Z
from magma.soccer_agent.model.game_state import PlaySide, PSoccerGameState
from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription
from magma.soccer_agent.model.world.soccer_world import SoccerWorld


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
