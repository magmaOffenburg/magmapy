from abc import ABC, abstractmethod
from enum import Enum
from typing import Final, Protocol

from magmapy.common.math.geometry.pose import P2D_ZERO, Pose2D
from magmapy.soccer_agent.model.game_state import PSoccerGameState
from magmapy.soccer_agent.model.world.soccer_world import PSoccerWorld


class ERoleSection(Enum):
    OUTER_LEFT = 3
    """The left outer field section."""

    LEFT = 2
    """The general left field section."""

    MIDDLE_LEFT = 1
    """The inner left mid-field section."""

    MIDDLE = 0
    """The general mid-field section."""

    MIDDLE_RIGHT = -1
    """The inner left mid-field section."""

    RIGHT = -2
    """The general right field section."""

    OUTER_RIGHT = -3
    """The right outer field section."""


class PRole(Protocol):
    """Protocol for roles."""

    @property
    def name(self) -> str:
        """The name of the role."""

    def get_target_pose(self) -> Pose2D:
        """Return the intended target pose."""


class PMutableRole(PRole, Protocol):
    """Protocol for mutable roles."""

    def get_priority(self) -> float:
        """Return the priority of the role."""

    def update(self, world: PSoccerWorld, game_state: PSoccerGameState) -> None:
        """Update the target position of the role based on the current game situation.

        Parameter
        ---------
        world : PSoccerWorld
            The soccer world.

        game_state : PSoccerGameState
            The current game state.
        """


class Role(ABC):
    """Base implementation for roles."""

    def __init__(self, name: str, priority: float) -> None:
        """Construct a new role."""

        self.name: Final[str] = name
        """The name of the role."""

        self.base_priority: Final[float] = priority
        """The (static) base priority of the role."""

        self._extra_priority: float = 0.0
        """The (dynamic) extra priority of the role."""

        self._target_pose: Pose2D = P2D_ZERO
        """The intended target pose."""

    def get_target_pose(self) -> Pose2D:
        """Return the intended target pose."""

        return self._target_pose

    def get_priority(self) -> float:
        """Return the priority of the role."""

        return self.base_priority + self._extra_priority

    def update(self, world: PSoccerWorld, game_state: PSoccerGameState) -> None:
        """Update the role.

        Parameter
        ---------
        world : PSoccerWorld
            The soccer world.

        game_state : PSoccerGameState
            The current game state.
        """

        # update target pose and extra priority
        self._target_pose = self._determine_target_pose(world, game_state)
        self._extra_priority = self._determine_extra_priority(world, game_state)

    @abstractmethod
    def _determine_target_pose(self, world: PSoccerWorld, game_state: PSoccerGameState) -> Pose2D:
        """Determine the target pose for the current game situation.

        Parameter
        ---------
        world : PSoccerWorld
            The soccer world.

        game_state : PSoccerGameState
            The current game state.
        """

    def _determine_extra_priority(self, world: PSoccerWorld, game_state: PSoccerGameState) -> float:
        """Determine the extra priority of this role and the current game situation.

        Note: Called after the target pose has been updated.

        Parameter
        ---------
        world : PSoccerWorld
            The soccer world.

        game_state : PSoccerGameState
            The current game state.
        """

        return 0.0
