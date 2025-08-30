from typing import Final

from magmapy.agent.model.belief import HysteresisBelief
from magmapy.common.math.geometry.angle import Angle2D
from magmapy.common.math.geometry.vector import Vector2D
from magmapy.soccer_agent.model.soccer_agent import PSoccerAgentModel


class AmIAtPosition(HysteresisBelief):
    """Belief for checking if we are at a certain position in the world."""

    def __init__(
        self,
        model: PSoccerAgentModel,
        target_pos: Vector2D,
        lower: float,
        upper: float,
    ) -> None:
        """Construct a new self position belief.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.

        target_pos : Vector2D
            The desired target position we want to be at.

        lower : float
            The distance below which the target position is considered to be reached.

        upper : float
            The distance above which the target position is considered to be left / not reached yet.
        """

        super().__init__(lower, upper, low_is_true=True)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        self.target_position: Vector2D = target_pos
        """The target position we want to be at."""

    def update(self) -> bool:
        distance_to_target = (self.target_position - self.model.get_world().get_this_player().get_position().as_2d()).norm()

        self._update_validity(distance_to_target, self.model.get_time())

        return self._valid


class AmIFacingDirection(HysteresisBelief):
    """Belief for checking if we are facing a certain direction in the world."""

    def __init__(
        self,
        model: PSoccerAgentModel,
        target_direction: Angle2D,
        lower: Angle2D,
        upper: Angle2D,
    ) -> None:
        """Construct a new facing direction belief.

        Parameter
        ---------
        model : PSoccerAgentModel
            The soccer agent model.

        target_direction : Angle2D
            The desired target direction we want to be facing.

        lower : Angle2D
            The angle deviation below which the target direction is considered to be reached.

        upper : Angle2D
            The angle deviation above which the target direction is considered to be left / not reached yet.
        """

        super().__init__(abs(lower.rad()), abs(upper.rad()), low_is_true=True)

        self.model: Final[PSoccerAgentModel] = model
        """The soccer agent model."""

        self.target_direction: Angle2D = target_direction
        """The target direction we want to be facing."""

    def update(self) -> bool:
        angle_deviation = self.target_direction - self.model.get_world().get_this_player().get_horizontal_angle()

        self._update_validity(abs(angle_deviation.rad()), self.model.get_time())

        return self._valid
