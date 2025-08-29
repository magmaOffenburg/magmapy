from typing import Final

from magma.common.math.geometry.angle import Angle2D, angle_from_to
from magma.common.math.geometry.pose import Pose2D
from magma.common.math.geometry.vector import Vector2D
from magma.soccer_agent.model.game_state import PSoccerGameState
from magma.soccer_agent.model.strategy.role import Role
from magma.soccer_agent.model.world.soccer_world import PSoccerWorld


class DummyRole(Role):
    """Simple role with a constant target pose and priority."""

    def __init__(
        self,
        rel_x: float,
        rel_y: float,
        theta: Angle2D | None = None,
        name: str = 'dummy',
        priority: float = 0.0,
    ) -> None:
        """Construct a new dummy role.

        Parameter
        ---------
        rel_x: float
            The relative field x-coordinate of the target position.

        rel_y: float
            The relative field y-coordinate of the target position.

        theta : Angle2D | None, default=None
            The fixed orientation of the role, or ``None`` to face the ball.

        name : str, default='dummy'
            The name of the role.

        priority : float, default=0.0
            The constant role priority.
        """

        super().__init__(name, priority)

        self.rel_x: Final[float] = rel_x
        """The field relative x-coordinate of the target position."""

        self.rel_y: Final[float] = rel_y
        """The field relative y-coordinate of the target position."""

        self.theta: Final[Angle2D | None] = theta
        """The constant relative field position."""

    def _determine_target_pose(self, world: PSoccerWorld, game_state: PSoccerGameState) -> Pose2D:
        field_area = world.get_map().get_field_area()
        target_pos = Vector2D(self.rel_x * field_area.max_x, self.rel_y * field_area.max_y)
        theta = angle_from_to(target_pos, world.get_ball().get_position()) if self.theta is None else self.theta

        return Pose2D(target_pos, theta)
