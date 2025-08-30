from typing import Final, Protocol, cast

from magmapy.soccer_agent.model.game_state import PlayModePhase, PSoccerGameState
from magmapy.soccer_agent.model.strategy.role import PMutableRole, PRole
from magmapy.soccer_agent.model.strategy.role_assignment import PRoleAssignmentStrategy
from magmapy.soccer_agent.model.strategy.strategy import PStrategyBook
from magmapy.soccer_agent.model.world.soccer_world import PSoccerWorld


class PRoleManager(Protocol):
    """Protocol for role managers."""

    def get_role(self) -> PRole | None:
        """Return the current role of the agent (if existing)."""


class PMutableRoleManager(PRoleManager, Protocol):
    """Protocol for mutable role managers."""

    def update(self, world: PSoccerWorld, game_state: PSoccerGameState) -> None:
        """Update the state of the model.

        Parameter
        ---------
        world : PSoccerWorld
            The soccer world representation.

        game_state : PSoccerGameState
            The current game state.
        """


class RoleManager:
    """Default role manager implementation."""

    def __init__(self, strategy_book: PStrategyBook, assignment_strategy: PRoleAssignmentStrategy) -> None:
        """Construct a new role manager.

        Parameter
        ---------
        strategy_book : PStrategyBook
            The team strategy book.

        assignment_strategy : PRoleAssignmentStrategy
            The role assignment strategy.
        """

        self._role: PRole | None = None
        """The current role of the agent (if existing)."""

        self.strategy_book: Final[PStrategyBook] = strategy_book
        """The strategy book defining available roles."""

        self.assignment_strategy: Final[PRoleAssignmentStrategy] = assignment_strategy
        """The dynamic role assignment strategy."""

    def get_role(self) -> PRole | None:
        """Return the current role of the agent (if existing)."""

        return self._role

    def update(self, world: PSoccerWorld, game_state: PSoccerGameState) -> None:
        """Update the state of the model.

        Parameter
        ---------
        world : PSoccerWorld
            The soccer world representation.

        game_state : PSoccerGameState
            The current game state.
        """

        # ----- Case 1: Incapable -----
        if world.get_this_player().incapable():
            # we are currently incapable --> no role
            self._role = None
            return

        # ----- Case 2: Goalie -----
        team_strategy = self.strategy_book.lookup_strategy(len(world.ifo().own_players_at_ball), game_state)
        goalie_role: PMutableRole | None = team_strategy.goalie_role
        if goalie_role is not None and world.get_this_player().is_goalie():
            # we are the goalie --> goalie role
            self._role = goalie_role
            self._role.update(world, game_state)
            return

        # ----- Case 3: Active Player -----
        trade_active_player_role = True
        if game_state.play_mode_phase == PlayModePhase.RUNNING:
            # do not trade the active player role when the game is running
            trade_active_player_role = False

            player_at_ball = world.ifo().get_own_player_at_ball()
            if player_at_ball == world.get_this_player():
                # we are the active player (the closest player to the ball of our team) --> active player role
                self._role = team_strategy.active_player_role
                self._role.update(world, game_state)
                return

        # ----- Case 4: Dynamic Role Assignment -----
        trade_goalie_role = False
        remaining_players = list(world.ifo().own_players_at_ball if trade_active_player_role else world.ifo().own_players_at_ball[1:])

        # remove goalie from remaining players in case there exists a goalie role
        if goalie_role is not None:
            # update role
            goalie_role.update(world, game_state)

            goalie = world.ifo().own_goalie

            if goalie is None:
                # no goalie in team --> trade goalie role
                trade_goalie_role = True

            else:
                if goalie in remaining_players:
                    # a goalie is among the remaining players --> remove it, as it is assigned its predefined goalie role
                    remaining_players.remove(goalie)

                # check if goalie needs replacement
                if game_state.play_mode_phase == PlayModePhase.RUNNING:
                    goalie_pos_deviation = (goalie.get_position().as_2d() - goalie_role.get_target_pose().pos).norm()

                    # TODO: update goalie-out-of-position truth value and trade the goalie role accordingly
                    trade_goalie_role = goalie_pos_deviation > 2.0

        # prepare collection of roles for remaining players
        available_roles = list(team_strategy.dynamic_roles)
        for role in available_roles:
            role.update(world, game_state)

        # prepend goalie role to the list of available roles in case it is open for trading (assuming it has been updated before)
        if trade_goalie_role:
            available_roles.insert(0, cast(PMutableRole, goalie_role))

        # append active player role to the list of available roles in case it is open for trading
        if trade_active_player_role:
            team_strategy.active_player_role.update(world, game_state)
            available_roles.append(team_strategy.active_player_role)

        # assign roles to remaining players
        assignments = self.assignment_strategy.assign_roles(remaining_players, available_roles)

        # fetch our role assignment
        self._role = assignments.get(world.get_this_player(), None)
