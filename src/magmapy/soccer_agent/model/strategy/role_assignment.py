from collections.abc import Mapping, Sequence
from typing import Protocol

from magmapy.soccer_agent.model.strategy.role import PRole
from magmapy.soccer_agent.model.world.soccer_objects import PSoccerPlayer


class PRoleAssignmentStrategy(Protocol):
    """Protocol for role assignment strategies."""

    def assign_roles(self, players: Sequence[PSoccerPlayer], roles: Sequence[PRole]) -> Mapping[PSoccerPlayer, PRole]:
        """Assign the given roles to the available players.

        Parameter
        ---------
        players : Sequence[PSoccerPlayer]
            The list of available players.

        roles : Sequence[PRole]
            The list of available roles.
        """


class RoleAssignmentStrategy:
    """Default role assignment strategy implementation."""

    def assign_roles(self, players: Sequence[PSoccerPlayer], roles: Sequence[PRole]) -> Mapping[PSoccerPlayer, PRole]:
        """Assign the given roles to the available players.

        Parameter
        ---------
        players : Sequence[PSoccerPlayer]
            The list of available players.

        roles : Sequence[PRole]
            The list of available roles.
        """

        # sort players by their player numbers
        sorted_players = list(players)
        sorted_players.sort(key=lambda player: player.player_no)

        return dict(zip(sorted_players, roles, strict=False))
