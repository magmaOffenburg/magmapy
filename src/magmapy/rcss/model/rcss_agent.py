from __future__ import annotations

from typing import TYPE_CHECKING

from magmapy.rcss.communication.rcss_perception import RCSSGameStatePerceptor
from magmapy.rcss.model.world.rcss_game_state import decode_rcss_play_mode
from magmapy.soccer_agent.model.game_state import PlaySide
from magmapy.soccer_agent.model.soccer_agent import SoccerAgentModel

if TYPE_CHECKING:
    from magmapy.agent.communication.perception import Perception
    from magmapy.agent.model.robot.robot_model import PMutableRobotModel
    from magmapy.soccer_agent.model.soccer_rules import SoccerRules
    from magmapy.soccer_agent.model.strategy.role_manager import PMutableRoleManager
    from magmapy.soccer_agent.model.world.soccer_world import PMutableSoccerWorld


class RCSSAgentModel(SoccerAgentModel):
    """The RoboCup Soccer Simulation (MuJoCo) specific agent model."""

    def __init__(
        self,
        robot: PMutableRobotModel,
        world: PMutableSoccerWorld,
        rules: SoccerRules,
        role_manager: PMutableRoleManager,
    ) -> None:
        """Construct a new soccer agent model.

        Parameter
        ---------
        robot : PMutableRobotModel
            The robot model representation.

        world : PMutableSoccerWorld
            The soccer world model.

        rules : SoccerRules
            The soccer rule book.

        role_manager : PRoleManager
            The role manager instance.
        """

        super().__init__(robot, world, rules, role_manager)

    def _update_game_state(self, perception: Perception) -> None:
        # fetch game state perceptor
        perceptor = perception.get_perceptor('game_state', RCSSGameStatePerceptor)
        if perceptor is None:
            return

        # buffer old play side for checking, if we switched sides
        prev_play_side = self._game_state.play_side

        # determine play side
        play_side = prev_play_side
        if perceptor.left_team == self._world.get_this_player().team_name:
            play_side = PlaySide.LEFT
        elif perceptor.right_team == self._world.get_this_player().team_name:
            play_side = PlaySide.RIGHT
        else:
            # we are not playing this game?!?
            pass

        # decode play mode and play mode phase
        play_mode, play_mode_phase = decode_rcss_play_mode(perceptor.play_mode, play_side)

        # fetch scores
        own_score = perceptor.score_left if play_side == PlaySide.LEFT else perceptor.score_right
        opponent_score = perceptor.score_right if play_side == PlaySide.LEFT else perceptor.score_left

        # update game state
        self._game_state.update(
            time=perception.get_time(),
            play_time=perceptor.play_time,
            play_side=play_side,
            play_mode=play_mode,
            play_mode_phase=play_mode_phase,
            own_score=own_score,
            opponent_score=opponent_score,
        )

        # check if a side switch occurred
        if play_side != prev_play_side:
            # TODO: mirror landmarks / world objects
            pass
