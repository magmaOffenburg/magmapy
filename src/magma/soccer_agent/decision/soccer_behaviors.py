from enum import Enum
from typing import Protocol, runtime_checkable

from magma.agent.decision.behavior import PBehavior
from magma.common.math.geometry.pose import Pose2D
from magma.common.math.geometry.vector import Vector2D


class SoccerBehaviorID(Enum):
    """Enum specifying soccer behavior names."""

    MOVE_TO = 'move_to'
    """The move-to behavior used to moving towards a desired 2D pose within the world."""

    MOVE_ALONG = 'move_along'
    """The move-along behavior used to moving along a desired 2D trajectory within the world."""

    NAVIGATE_TO = 'navigate_to'
    """The navigate-to behavior used to navigate towards a desired 2D pose while respecting obstacles within the world."""

    PENALTY_POSITIONING = 'penalty_positioning'
    """The penalty-positioning behavior used to move the agent in a passive position while the other team takes a penalty kick."""

    KICK_OFF_POSITIONING = 'kick_off_positioning'
    """The kick-off-positioning behavior used to move the agent in an appropriate position for kick-off."""

    ATTACK = 'attack'
    """The attack behavior used to approach the ball and kicking it somewhere."""

    DRIBBLE = 'dribble'
    """The dribble behavior used to walk straight with the ball."""


@runtime_checkable
class PMoveToBehavior(PBehavior, Protocol):
    """Protocol for move-to behaviors."""

    def set(self, target_pose: Pose2D) -> None:
        """Set the desired target pose to move to.

        Parameter
        ---------
        target_pose : Pose2D
            The global target pose.
        """


@runtime_checkable
class PMoveAlongBehavior(PBehavior, Protocol):
    """Protocol for move-along behaviors."""

    def set(self, target_trajectory: list[Pose2D]) -> None:
        """Set the desired target trajectory to move along.

        Parameter
        ---------
        target_trajectory : list[Pose2D]
            The global target trajectory.
        """


@runtime_checkable
class PKickBehavior(PBehavior, Protocol):
    """Protocol for kick behaviors."""

    def set(self, target_position: Vector2D, *, is_goal_kick: bool = False) -> None:
        """Set the desired target position to kick.

        Parameter
        ---------
        target_position : Vector2D
            The global target kick position.

        is_goal_kick : bool, default=False
            Flag indicating if the intended kick is a goal kick.
        """

    def get_relative_move_to_pose(self) -> Pose2D:
        """Return the move-to pose relative to the ball and intended kick direction in order to perform this kick."""

    def get_applicability(self) -> float:
        """Return the applicability of the kick.

        Returns
        -------
        utility : float
            **Negative values** indicate that the kick is not applicable in the current game situation.
            A **positive value** indicates that the kick in general is applicable in the current game situation and represent a measurement of how well it fits the requested kick.
        """

    def get_executability(self) -> float:
        """Return the executability of the kick.

        Returns
        -------
        utility : float
            **Negative values** indicate that performing the kick is expected to **not hit the ball** and should therefore not be performed.
            A **positive value** indicates that the kick **should be able to hit the ball** and represents a measurement of how well it fits the kick (0 = worst; 1 = optimal).
        """
