from collections.abc import Sequence
from typing import Final, Protocol

from magma.soccer_agent.model.game_state import PSoccerGameState
from magma.soccer_agent.model.strategy.role import PMutableRole


class TeamStrategy:
    """Team strategy definition."""

    def __init__(
        self,
        name: str,
        goalie_role: PMutableRole | None,
        dynamic_roles: Sequence[PMutableRole],
        active_player_role: PMutableRole,
    ):
        """construct a new team strategy."""

        self.name: Final[str] = name
        """The name of the team strategy."""

        self.goalie_role: Final[PMutableRole | None] = goalie_role
        """The goalie role."""

        self.dynamic_roles: Final[Sequence[PMutableRole]] = dynamic_roles
        """The roles for the remaining players."""

        self.active_player_role: Final[PMutableRole] = active_player_role
        """The active player role."""


class PStrategyBook(Protocol):
    """Protocol for team strategy books."""

    @property
    def name(self) -> str:
        """The name of the team strategy book."""

    def lookup_strategy(self, num_players: int, game_state: PSoccerGameState) -> TeamStrategy:
        """Lookup a team strategy for the current game situation.

        Parameter
        ---------
        num_players : int
            The total number of active / capable players in our team.

        game_state : PSoccerGameState
            The current game state.
        """


class SingletonStrategyBook:
    """A simple strategy book consisting of a single team strategy."""

    def __init__(self, team_strategy: TeamStrategy) -> None:
        """Construct a new singleton strategy book."""

        self.team_strategy: Final[TeamStrategy] = team_strategy
        """The one and only team strategy."""

    @property
    def name(self) -> str:
        return self.team_strategy.name

    def lookup_strategy(self, num_players: int, game_state: PSoccerGameState) -> TeamStrategy:
        """Lookup a team strategy for the current game situation.

        Parameter
        ---------
        num_players : int
            The total number of active / capable players in our team.

        game_state : PSoccerGameState
            The current game state.
        """

        return self.team_strategy
