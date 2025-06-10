from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from magma.common.math.geometry.bounding_box import AABB2D
from magma.common.math.geometry.vector import Vector2D, Vector3D
from magma.common.util.map.feature.feature_map import FeatureMap, PFeatureMap
from magma.common.util.map.feature.features import LineFeature, PLineFeature, PointFeature, PPointFeature

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magma.soccer_agent.model.world.soccer_field_description import PSoccerFieldDescription


class PSoccerMap(PFeatureMap, Protocol):
    """Protocol for a soccer map."""

    def get_field_dimensions(self) -> Vector2D:
        """Retrieve the soccer field dimensions."""

    def get_field_half_length(self) -> float:
        """Half of the soccer field length (x-coordinate)."""

    def get_field_half_width(self) -> float:
        """Half of the soccer field width (y-coordinate)."""

    def get_goal_dimensions(self) -> Vector3D:
        """Retrieve the goal dimensions."""

    def get_goal_half_width(self) -> float:
        """Half of the goal width (y-coordinate)."""

    def get_goal_depth(self) -> float:
        """Depth of the goal (x-coordinate)."""

    def get_goal_height(self) -> float:
        """Height of the goal (z-coordinate)."""

    def get_goalie_area_dimensions(self) -> Vector2D:
        """Retrieve the goalie area dimensions."""

    def get_goalie_area_half_width(self) -> float:
        """Half of the goalie area width (y-coordinate)."""

    def get_goalie_area_depth(self) -> float:
        """Depth of the goalie area area (x-coordinate)."""

    def get_penalty_area_dimensions(self) -> Vector2D:
        """Retrieve the penalty area dimensions."""

    def get_penalty_area_half_width(self) -> float:
        """Half of the penalty area width (y-coordinate)."""

    def get_penalty_area_depth(self) -> float:
        """Depth of the penalty area (x-coordinate)."""

    def get_middle_circle_radius(self) -> float:
        """Retrieve the radius of the middle circle."""

    def get_penalty_spot_distance(self) -> float:
        """Retrieve the distance of the penalty spot from the goal line."""

    def get_own_goal_position(self) -> Vector3D:
        """Retrieve the position of the own goal."""

    def get_opponent_goal_position(self) -> Vector3D:
        """Retrieve the position of the opponent goal."""

    def get_own_penalty_spot_position(self) -> Vector3D:
        """Retrieve the position of the own penalty spot (in front of our goal)."""

    def get_opponent_penalty_spot_position(self) -> Vector3D:
        """Retrieve the position of the opponent penalty spot (in front of the opponent goal)."""

    def get_field_area(self) -> AABB2D:
        """Retrieve the soccer field area."""

    def get_own_goal_area(self) -> AABB2D:
        """Retrieve the own goal area."""

    def get_opponent_goal_area(self) -> AABB2D:
        """Retrieve the opponent goal area."""

    def get_own_goalie_area(self) -> AABB2D:
        """Retrieve the own goalie area."""

    def get_opponent_goalie_area(self) -> AABB2D:
        """Retrieve the opponent goalie area."""

    def get_own_penalty_area(self) -> AABB2D:
        """Retrieve the own penalty area."""

    def get_opponent_penalty_area(self) -> AABB2D:
        """Retrieve the opponent penalty area."""


class SoccerMap(FeatureMap):
    """Class representing a soccer field."""

    def __init__(
        self,
        field_dim: Vector2D,
        goal_dim: Vector3D,
        goalie_area_dim: Vector2D,
        penalty_area_dim: Vector2D,
        middle_circle_radius: float,
        penalty_spot_distance: float,
        point_features: Sequence[PPointFeature] | None = None,
        line_features: Sequence[PLineFeature] | None = None,
    ) -> None:
        """Construct a new soccer feature map."""

        super().__init__(point_features, line_features)

        self._field_dimensions: Vector2D = field_dim
        self._goal_dimensions: Vector3D = goal_dim
        self._goalie_area_dimensions: Vector2D = goalie_area_dim
        self._penalty_area_dimensions: Vector2D = penalty_area_dim
        self._middle_circle_radius: float = middle_circle_radius
        self._penalty_spot_distance: float = penalty_spot_distance

        field_half_x = field_dim.x / 2

        self._field_area: AABB2D = AABB2D(-field_half_x, field_half_x, -field_dim.y / 2, field_dim.y / 2)
        self._own_goal_area: AABB2D = AABB2D(-field_half_x - goal_dim.x, -field_half_x, -goal_dim.y / 2, goal_dim.y / 2)
        self._opponent_goal_area: AABB2D = AABB2D(field_half_x, field_half_x + goal_dim.x, -goal_dim.y / 2, goal_dim.y / 2)
        self._own_goalie_area: AABB2D = AABB2D(-field_half_x, -field_half_x + goalie_area_dim.x, -goalie_area_dim.y / 2, goalie_area_dim.y / 2)
        self._opponent_goalie_area: AABB2D = AABB2D(field_half_x - goalie_area_dim.x, field_half_x, -goalie_area_dim.y / 2, goalie_area_dim.y / 2)
        self._own_penalty_area: AABB2D = AABB2D(-field_half_x, -field_half_x + penalty_area_dim.x, -penalty_area_dim.y / 2, penalty_area_dim.y / 2)
        self._opponent_penalty_area: AABB2D = AABB2D(field_half_x - penalty_area_dim.x, field_half_x, -penalty_area_dim.y / 2, penalty_area_dim.y / 2)

        self._own_goal_position: Vector3D = Vector3D(-field_half_x, 0, 0)
        self._opponent_goal_position: Vector3D = Vector3D(field_half_x, 0, 0)
        self._own_penalty_spot_position: Vector3D = Vector3D(-field_half_x + penalty_spot_distance, 0, 0)
        self._opponent_penalty_spot_position: Vector3D = Vector3D(field_half_x - penalty_spot_distance, 0, 0)

    @staticmethod
    def from_description(desc: PSoccerFieldDescription) -> SoccerMap:
        """Construct a new soccer feature map from the given field description."""

        s_map: SoccerMap = SoccerMap(
            desc.get_field_dimensions(),
            desc.get_goal_dimensions(),
            desc.get_goalie_area_dimensions(),
            desc.get_penalty_area_dimensions(),
            desc.get_middle_circle_radius(),
            desc.get_penalty_spot_distance(),
        )
        s_map.set_point_features(tuple(PointFeature(f.name, f.get_type(), f.get_known_position()) for f in desc.get_point_features()))
        s_map.set_line_features(tuple(LineFeature(f.name, f.get_type(), f.get_known_position1(), f.get_known_position2()) for f in desc.get_line_features()))

        return s_map

    def get_field_dimensions(self) -> Vector2D:
        """Retrieve the soccer field dimensions."""

        return self._field_dimensions

    def get_field_half_length(self) -> float:
        """Half of the soccer field length (x-coordinate)."""

        return self._field_dimensions.x / 2

    def get_field_half_width(self) -> float:
        """Half of the soccer field width (y-coordinate)."""

        return self._field_dimensions.y / 2

    def get_goal_dimensions(self) -> Vector3D:
        """Retrieve the goal dimensions."""

        return self._goal_dimensions

    def get_goal_half_width(self) -> float:
        """Half of the goal width (y-coordinate)."""

        return self._goal_dimensions.y / 2

    def get_goal_depth(self) -> float:
        """Depth of the goal (x-coordinate)."""

        return self._goal_dimensions.x

    def get_goal_height(self) -> float:
        """Height of the goal (z-coordinate)."""

        return self._goal_dimensions.z

    def get_goalie_area_dimensions(self) -> Vector2D:
        """Retrieve the goalie area dimensions."""

        return self._goalie_area_dimensions

    def get_goalie_area_half_width(self) -> float:
        """Half of the goalie area width (y-coordinate)."""

        return self._goalie_area_dimensions.y

    def get_goalie_area_depth(self) -> float:
        """Depth of the goalie area area (x-coordinate)."""

        return self._goalie_area_dimensions.x

    def get_penalty_area_dimensions(self) -> Vector2D:
        """Retrieve the penalty area dimensions."""

        return self._penalty_area_dimensions

    def get_penalty_area_half_width(self) -> float:
        """Half of the penalty area width (y-coordinate)."""

        return self._penalty_area_dimensions.y

    def get_penalty_area_depth(self) -> float:
        """Depth of the penalty area (x-coordinate)."""

        return self._penalty_area_dimensions.x

    def get_middle_circle_radius(self) -> float:
        """Retrieve the radius of the middle circle."""

        return self._middle_circle_radius

    def get_penalty_spot_distance(self) -> float:
        """Retrieve the distance of the penalty spot from the goal line."""

        return self._penalty_spot_distance

    def get_own_goal_position(self) -> Vector3D:
        """Retrieve the position of the own goal."""

        return self._own_goal_position

    def get_opponent_goal_position(self) -> Vector3D:
        """Retrieve the position of the opponent goal."""

        return self._opponent_goal_position

    def get_own_penalty_spot_position(self) -> Vector3D:
        """Retrieve the position of the own penalty spot (in front of our goal)."""

        return self._own_penalty_spot_position

    def get_opponent_penalty_spot_position(self) -> Vector3D:
        """Retrieve the position of the opponent penalty spot (in front of the opponent goal)."""

        return self._opponent_penalty_spot_position

    def get_field_area(self) -> AABB2D:
        """Retrieve the soccer field area."""

        return self._field_area

    def get_own_goal_area(self) -> AABB2D:
        """Retrieve the own goal area."""

        return self._own_goal_area

    def get_opponent_goal_area(self) -> AABB2D:
        """Retrieve the opponent goal area."""

        return self._opponent_goal_area

    def get_own_goalie_area(self) -> AABB2D:
        """Retrieve the own goalie area."""

        return self._own_goalie_area

    def get_opponent_goalie_area(self) -> AABB2D:
        """Retrieve the opponent goalie area."""

        return self._opponent_goalie_area

    def get_own_penalty_area(self) -> AABB2D:
        """Retrieve the own penalty area."""

        return self._own_penalty_area

    def get_opponent_penalty_area(self) -> AABB2D:
        """Retrieve the opponent penalty area."""

        return self._opponent_penalty_area
