from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from magma.agent.model.world.objects import MovableObject

if TYPE_CHECKING:
    from magma.common.math.geometry.vector import Vector3D


class PSoccerBall(Protocol):
    """Protocol for a soccer ball object."""

    def get_radius(self) -> float:
        """Retrieve the radius of the ball."""


class PSoccerPlayer(Protocol):
    """Protocol for soccer players."""

    def get_team(self) -> str:
        """Retrieve the team name of the player."""

    def get_player_no(self) -> int:
        """Retrieve the player number of the player."""

    def is_own_team(self) -> bool:
        """Flag representing if the player is our teammate."""


class PThisSoccerPlayer(PSoccerPlayer, Protocol):
    """Protocol for the soccer player representing this agent."""


class SoccerBall(MovableObject):
    """Default representation of a soccer ball in a soccer game."""

    def __init__(
        self,
        radius: float,
        position: Vector3D | None = None,
        velocity: Vector3D | None = None,
    ) -> None:
        """Construct a new soccer ball object.

        Parameter
        ---------
        radius : float
            The radius of the ball.

        position : Vector3D | None, default=None
            The initial position of the ball.

        velocity : Vector3D | None, default=None
            The initial velocity of the ball.
        """

        super().__init__('ball', position, velocity)

        self._radius = radius
        """The radius of the ball."""

    def get_radius(self) -> float:
        """Retrieve the radius of the ball."""

        return self._radius


class SoccerPlayer(MovableObject):
    """Default representation of a soccer player in a soccer match."""

    def __init__(
        self,
        team_name: str,
        player_no: int,
        *,
        own_team: bool,
        position: Vector3D | None = None,
        velocity: Vector3D | None = None,
    ) -> None:
        """Construct a new soccer player object.

        Parameter
        ---------
        team_name : str
            The name of the team the player belongs to.

        player_no : int
            The player number.

        own_team : bool
            True, if the player is in our team, False if it belongs to the opponent team.

        position : Vector3D | None, default=None
            The initial position of the player.

        velocity : Vector3D | None, default=None
            The initial velocity of the player.
        """

        super().__init__(f'{team_name}{player_no}', position, velocity)

        self._team_name: str = team_name
        """The name of the team this player belongs to."""

        self._player_no: int = player_no
        """The player number."""

        self._own_team: bool = own_team
        """Flag indicating if the player is in our team or not."""

    def get_team(self) -> str:
        """Retrieve the team name of the player."""

        return self._team_name

    def get_player_no(self) -> int:
        """Retrieve the player number of the player."""

        return self._player_no

    def is_own_team(self) -> bool:
        """Flag representing if the player is our team mate."""

        return self._own_team


class ThisSoccerPlayer(SoccerPlayer):
    """Default this-soccer-player implementation."""

    def __init__(
        self,
        team_name: str,
        player_no: int,
        position: Vector3D | None = None,
        velocity: Vector3D | None = None,
    ) -> None:
        """Construct a new this-soccer-player.

        Parameter
        ---------
        team_name: str
            Our team name.

        player_no: int,
            Our player number.

        position : Vector3D | None, default=None
            The initial position of ourself.

        velocity : Vector3D | None, default=None
            The initial velocity of ourself.
        """

        super().__init__(team_name, player_no, own_team=True, position=position, velocity=velocity)
