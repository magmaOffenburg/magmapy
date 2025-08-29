from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magma.agent.model.agent_model import PAgentModel, PMutableAgentModel
from magma.rchl.communication.rchl_perception import RCHLGameStatePerceptor
from magma.rchl.model.rchl_game_state import decode_rchl_game_state
from magma.soccer_agent.model.game_state import PlaySide
from magma.soccer_agent.model.soccer_agent import SoccerAgentModel

if TYPE_CHECKING:
    from magma.agent.communication.perception import Perception
    from magma.agent.model.robot.robot_model import PMutableRobotModel
    from magma.soccer_agent.model.soccer_rules import SoccerRules
    from magma.soccer_agent.model.strategy.role_manager import PMutableRoleManager
    from magma.soccer_agent.model.world.soccer_world import PMutableSoccerWorld


@runtime_checkable
class PRCHLAgentModel(PAgentModel, Protocol):
    """Protocol for RocoCup Soccer Humanoid League agent models."""


@runtime_checkable
class PMutableRCSSAgentModel(PRCHLAgentModel, PMutableAgentModel, Protocol):
    """Protocol for mutable RoboCup Soccer Humanoid League agent models."""


class RCHLAgentModel(SoccerAgentModel):
    """The RoboCup Soccer Humanoid League specific agent model."""

    def __init__(
        self,
        robot: PMutableRobotModel,
        world: PMutableSoccerWorld,
        rules: SoccerRules,
        role_manager: PMutableRoleManager,
        team_id: int,
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

        team_id : int
            Our Humanoid League team id.
        """

        super().__init__(robot, world, rules, role_manager)

        self.team_id: Final[int] = team_id
        """The id of our team in the Humanoid League."""

    def _update_game_state(self, perception: Perception) -> None:
        # fetch game state perceptor
        perceptor = perception.get_perceptor('game_state', RCHLGameStatePerceptor)
        if perceptor is None:
            return

        if len(perceptor.teams) < 2:
            # expected to receive two team information
            return

        # fetch team information
        if perceptor.teams[0].team_number == self.team_id:
            own_team_info = perceptor.teams[0]
            opponent_team_info = perceptor.teams[1]
            play_side = PlaySide.LEFT
        elif perceptor.teams[1].team_number == self.team_id:
            own_team_info = perceptor.teams[1]
            opponent_team_info = perceptor.teams[0]
            play_side = PlaySide.RIGHT
        else:
            # we are receiving data which is not related to our team
            return

        # buffer old play side for checking, if we switched sides
        prev_play_side = self._game_state.play_side

        # calculate play time
        play_time = 600.0 - perceptor.secs_remaining

        # decode play mode and play mode phase
        our_kick_off = perceptor.kick_off_team == self.team_id
        our_secondary_state = perceptor.secondary_state_info.team_number == self.team_id
        play_mode, play_mode_phase = decode_rchl_game_state(perceptor.state, perceptor.secondary_state, perceptor.secondary_state_info.sub_mode, our_kick_off=our_kick_off, our_secondary_state=our_secondary_state)

        # update game state
        self._game_state.update(
            time=perception.get_time(),
            play_time=play_time,
            play_side=play_side,
            play_mode=play_mode,
            play_mode_phase=play_mode_phase,
            own_score=own_team_info.score,
            opponent_score=opponent_team_info.score,
        )

        # check if a side switch occurred
        if play_side != prev_play_side:
            # TODO: mirror location of world objects
            pass
