from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol

from magma.agent.model.world.objects import InformationSource, MovableObject, PMovableObject

if TYPE_CHECKING:
    from magma.common.math.geometry.rotation import Rotation3D
    from magma.common.math.geometry.vector import Vector3D


class PSoccerBall(PMovableObject, Protocol):
    """Protocol for a soccer ball object."""

    @property
    def radius(self) -> float:
        """The radius of the ball."""


class PSoccerPlayer(PMovableObject, Protocol):
    """Protocol for soccer players."""

    @property
    def team_name(self) -> str:
        """The name of the team the player belongs to."""

    @property
    def player_no(self) -> int:
        """The player number of the player."""

    @property
    def own_team(self) -> bool:
        """Flag representing if the player is our teammate."""

    def is_goalie(self) -> bool:
        """Check if the player is the goalie."""

    def incapable(self) -> bool:
        """Check if the player in incapable."""


class PThisSoccerPlayer(PSoccerPlayer, Protocol):
    """Protocol for the soccer player representing this agent."""


class SoccerBall(MovableObject):
    """Default representation of a soccer ball in a soccer game."""

    def __init__(
        self,
        radius: float,
        position: Vector3D | None = None,
        orientation: Rotation3D | None = None,
    ) -> None:
        """Construct a new soccer ball object.

        Parameter
        ---------
        radius : float
            The radius of the ball.

        position : Vector3D | None, default=None
            The initial position of the soccer ball.
            If ``None``, the global position is initialized to zero.

        orientation : Rotation3D | None, default=None
            The initial global orientation of the soccer ball.
            If ``None``, the global orientation is initialized to the identity.
        """

        super().__init__('ball', position, orientation)

        self.radius: Final[float] = radius
        """The radius of the ball."""


class SoccerPlayer(MovableObject):
    """Default representation of a soccer player in a soccer match."""

    def __init__(
        self,
        team_name: str,
        player_no: int,
        *,
        own_team: bool,
        is_goalie: bool | None = None,
        position: Vector3D | None = None,
        orientation: Rotation3D | None = None,
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
            If ``None``, the global position is initialized to zero.

        orientation : Rotation3D | None, default=None
            The initial global orientation of the player.
            If ``None``, the global orientation is initialized to the identity.
        """

        super().__init__(f'{team_name}{player_no}', position, orientation)

        self.team_name: Final[str] = team_name
        """The name of the team this player belongs to."""

        self.player_no: Final[int] = player_no
        """The player number."""

        self.own_team: Final[bool] = own_team
        """Flag indicating if the player is in our team or not."""

        self._is_goalie: bool = player_no == 1 if is_goalie is None else is_goalie
        """Flag representing if the player is the goalie."""

    def is_goalie(self) -> bool:
        """Check if the player is the goalie."""

        return self._is_goalie

    def incapable(self) -> bool:
        """Check if the player in incapable."""

        return False


class ThisSoccerPlayer(SoccerPlayer):
    """Default this-soccer-player implementation."""

    def __init__(self, team_name: str, player_no: int) -> None:
        """Construct a new this-soccer-player.

        Parameter
        ---------
        team_name: str
            Our team name.

        player_no: int,
            Our player number.
        """

        super().__init__(team_name, player_no, own_team=True)

    def update_location(
        self,
        time: float,
        pos: Vector3D,
        orientation: Rotation3D,
    ) -> None:
        """Update the state of the visible object.

        Parameter
        ---------
        time: float
            The current time.

        pos: Vector3D
            The estimated global position.

        orientation: Rotation3D, default=R3D_IDENTITY
            The estimated global orientation.
        """

        super().update(time, InformationSource.NONE, pos, orientation)
