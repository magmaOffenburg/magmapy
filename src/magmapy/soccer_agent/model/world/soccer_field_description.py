from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from magmapy.common.util.map.feature.features import LineFeature, PLineFeature, PointFeature, PPointFeature

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magmapy.common.math.geometry.vector import Vector2D, Vector3D


class PSoccerFieldDescription(Protocol):
    """Protocol for a soccer field description."""

    def get_field_dimensions(self) -> Vector2D:
        """Retrieve the soccer field dimensions."""

    def get_goal_dimensions(self) -> Vector3D:
        """Retrieve the goal dimensions."""

    def get_goalie_area_dimensions(self) -> Vector2D:
        """Retrieve the goalie area dimensions."""

    def get_penalty_area_dimensions(self) -> Vector2D:
        """Retrieve the penalty area dimensions."""

    def get_middle_circle_radius(self) -> float:
        """Retrieve the radius of the middle circle."""

    def get_penalty_spot_distance(self) -> float:
        """Retrieve the distance of the penalty spot from the goal line."""

    def get_point_features(self) -> Sequence[PPointFeature]:
        """Retrieve the known point features of the field."""

    def get_line_features(self) -> Sequence[PLineFeature]:
        """Retrieve the known line features of the field."""


class SoccerFieldDescription:
    """Class describing a soccer field and its visible features."""

    def __init__(
        self,
        field_dim: Vector2D,
        goal_dim: Vector3D,
        goalie_area_dim: Vector2D,
        penalty_area_dim: Vector2D,
        middle_circle_radius: float,
        penalty_spot_distance: float,
    ) -> None:
        """Construct a new soccer field description."""

        super().__init__()

        self._field_dimensions: Vector2D = field_dim
        self._goal_dimensions: Vector3D = goal_dim
        self._goalie_area_dimensions: Vector2D = goalie_area_dim
        self._penalty_area_dimensions: Vector2D = penalty_area_dim
        self._middle_circle_radius: float = middle_circle_radius
        self._penalty_spot_distance: float = penalty_spot_distance

        self._point_features: dict[str, PPointFeature] = {}
        self._line_features: dict[str, PLineFeature] = {}

    def get_field_dimensions(self) -> Vector2D:
        """Retrieve the soccer field dimensions."""

        return self._field_dimensions

    def get_goal_dimensions(self) -> Vector3D:
        """Retrieve the goal dimensions."""

        return self._goal_dimensions

    def get_goalie_area_dimensions(self) -> Vector2D:
        """Retrieve the goalie area dimensions."""

        return self._goalie_area_dimensions

    def get_penalty_area_dimensions(self) -> Vector2D:
        """Retrieve the penalty area dimensions."""

        return self._penalty_area_dimensions

    def get_middle_circle_radius(self) -> float:
        """Retrieve the radius of the middle circle."""

        return self._middle_circle_radius

    def get_point_features(self) -> Sequence[PPointFeature]:
        """Retrieve the known point features of the field."""

        return tuple(self._point_features.values())

    def _add_point(self, name: str, f_type: str, known_pos: Vector3D) -> None:
        """Add a new point feature to the field.

        Parameter
        ---------
        name : str
            The name of the point feature.

        f_type : str
            The type of point feature.

        known_pos : Vector3D
            The known position of the point feature.
        """

        if name in self._point_features:
            print(f'WARNING: A point feature with the name {name} has already been specified!')  # noqa: T201

        self._point_features[name] = PointFeature(name, f_type, known_pos)

    def get_penalty_spot_distance(self) -> float:
        """Retrieve the distance of the penalty spot from the goal line."""

        return self._penalty_spot_distance

    def get_line_features(self) -> Sequence[PLineFeature]:
        """Retrieve the known line features of the field."""

        return tuple(self._line_features.values())

    def _add_line(self, name: str, f_type: str, known_pos1: Vector3D, known_pos2: Vector3D) -> None:
        """Add a new line feature to the field.

        Parameter
        ---------
        name : str
            The name of the line.

        f_type : str
            The type of tine feature.

        known_pos1 : Vector3D
            The first known position of the line.

        known_pos2 : Vector3D
            The second known position of the line.
        """

        if name in self._line_features:
            print(f'WARNING: A line feature with the name {name} has already been specified!')  # noqa: T201

        self._line_features[name] = LineFeature(name, f_type, known_pos1, known_pos2)
