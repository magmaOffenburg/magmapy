from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable

from magma.agent.decision.behavior import PBehavior
from magma.common.math.geometry.angle import Angle2D
from magma.common.math.geometry.bounding_box import AABB2D
from magma.common.math.geometry.interval import Interval
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


@dataclass(frozen=True)
class KickParameter:
    """Class representing a parameter set for a kick behavior.

    Most kick parameter are specified in a coordinate system with the ball as its origin facing the intended kick direction.
    """

    direction: Angle2D
    """The kick direction relative to the base body."""

    distance_interval: Interval
    """The kick distance interval (minimum and maximum kick distance) this kick is able to perform."""

    opponent_interval: Interval
    """
    The distance interval (minimum and maximum distance) the closest opponent has to be within for this kick to be applicable.
    If the closes opponent is closer than the minimum distance or farther away than the maximum distance, this kick will not be applicable.
    """

    base_priority: float
    """The base priority of the kick."""

    relative_move_to_pose: Pose2D
    """The target pose to move to when preparing for the kick."""

    relative_support_foot_pose: Pose2D
    """The optimal pose of the supporting foot for performing the kick."""

    kickable_area: AABB2D
    """The kickable area."""

    theta_range: Angle2D
    """The maximum allowed angular deviation from the desired kick direction this kick is able to handle."""

    tolerance_factor: float
    """Factor used to parameterize hysteresis functions (e.g. the factor by which the kickable area is extended to check if it has been left again)."""


@runtime_checkable
class PKickBehavior(PBehavior, Protocol):
    """Protocol for kick behaviors."""

    def get_params(self) -> KickParameter:
        """Return the kick parameter set."""

    def set(self, target_position: Vector2D, *, is_goal_kick: bool = False) -> None:
        """Set the desired target position to kick.

        Parameter
        ---------
        target_position : Vector2D
            The global target kick position.

        is_goal_kick : bool, default=False
            Flag indicating if the intended kick is a goal kick.
        """
