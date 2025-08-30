from __future__ import annotations

from enum import Enum

from magmapy.common.math.geometry.vector import V2D_ZERO, Vector2D, Vector3D
from magmapy.soccer_agent.model.world.soccer_field_description import SoccerFieldDescription


class RCSSFieldVersion(Enum):
    """Enum specifying the available RoboCup Humanoid Soccer league field versions."""

    UNKNOWN = 'unknown'
    """Unknown field version."""

    ADULT_2014 = 'hl_adult_2014'
    """2014 version of the Adult Size soccer field."""

    ADULT_2019 = 'hl_adult_2019'
    """2019 version of the Adult Size soccer field."""

    ADULT_2020 = 'hl_adult_2020'
    """2020 version of the Adult Size soccer field."""

    @staticmethod
    def from_value(version: str) -> RCSSFieldVersion:
        """Fetch the enum entry corresponding to the given version value."""

        for v in RCSSFieldVersion:
            if v.value == version:
                return v

        print(f'WARNING: Unknown HL field version: "{version}"!')  # noqa: T201

        return RCSSFieldVersion.UNKNOWN

    @staticmethod
    def create_description_for(version: str) -> SoccerFieldDescription:
        """Create a field description for the given field version."""

        version_id = RCSSFieldVersion.from_value(version)

        if version_id == RCSSFieldVersion.ADULT_2014:
            return RCSSField2014()
        if version_id == RCSSFieldVersion.ADULT_2019:
            return RCSSField2019()

        # cases: ADULT_2020 and UNKNOWN
        return RCSSField2020()


class RCSSField2014(SoccerFieldDescription):
    """Class representing the soccer field used by the RoboCup Humanoid Adult Size in 2014 to 2018."""

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """Construct a new soccer field description."""

        super().__init__(
            Vector2D(9.0, 6.0) if field_dim is None else field_dim,
            Vector3D(0.6, 2.6, 1.8) if goal_dim is None else goal_dim,
            Vector2D(1.0, 5.0) if goalie_area_dim is None else goalie_area_dim,
            V2D_ZERO if penalty_area_dim is None else penalty_area_dim,
            0.75 if middle_circle_radius is None else middle_circle_radius,
            2.1 if penalty_spot_distance is None else penalty_spot_distance,
        )

        field_half_x = self._field_dimensions.x / 2
        field_half_y = self._field_dimensions.y / 2
        goal_half_y = self._goal_dimensions.y / 2
        ga_half_y = self._goalie_area_dimensions.y / 2
        pa_half_y = self._penalty_area_dimensions.y / 2

        has_goalie_area = self._goalie_area_dimensions.x > 0 and self._goalie_area_dimensions.y > 0
        has_penalty_area = self._penalty_area_dimensions.x > 0 and self._penalty_area_dimensions.y > 0

        # fmt: off
        # init landmarks
        l_type = 't_junction'
        self._add_point('t_cuf', l_type, Vector3D(0.0,  field_half_y, 0.0))   # T-junction center upper field
        self._add_point('t_clf', l_type, Vector3D(0.0, -field_half_y, 0.0))   # T-junction center lower field
        if has_penalty_area:
            self._add_point('t_lupa', l_type, Vector3D(-field_half_x,  pa_half_y, 0.0))   # T-junction left upper penalty area
            self._add_point('t_llpa', l_type, Vector3D(-field_half_x, -pa_half_y, 0.0))   # T-junction left lower penalty area
            self._add_point('t_rupa', l_type, Vector3D( field_half_x,  pa_half_y, 0.0))   # T-junction right upper penalty area
            self._add_point('t_rlpa', l_type, Vector3D( field_half_x, -pa_half_y, 0.0))   # T-junction right lower penalty area
        if has_goalie_area:
            self._add_point('t_luga', l_type, Vector3D(-field_half_x,  ga_half_y, 0.0))   # T-junction left upper goalie area
            self._add_point('t_llga', l_type, Vector3D(-field_half_x, -ga_half_y, 0.0))   # T-junction left lower goalie area
            self._add_point('t_ruga', l_type, Vector3D( field_half_x,  ga_half_y, 0.0))   # T-junction right upper goalie area
            self._add_point('t_rlga', l_type, Vector3D( field_half_x, -ga_half_y, 0.0))   # T-junction right lower goalie area

        l_type = 'l_junction'
        self._add_point('l_luf', l_type, Vector3D(-field_half_x,  field_half_y, 0.0))     # L-junction left upper field
        self._add_point('l_llf', l_type, Vector3D(-field_half_x, -field_half_y, 0.0))     # L-junction left lower field
        self._add_point('l_ruf', l_type, Vector3D( field_half_x,  field_half_y, 0.0))     # L-junction right upper field
        self._add_point('l_rlf', l_type, Vector3D( field_half_x, -field_half_y, 0.0))     # L-junction right lower field
        if has_penalty_area:
            self._add_point('l_lupa', l_type, Vector3D(-field_half_x + self._penalty_area_dimensions.x,  pa_half_y, 0.0))    # L-junction left upper penalty area
            self._add_point('l_llpa', l_type, Vector3D(-field_half_x + self._penalty_area_dimensions.x, -pa_half_y, 0.0))    # L-junction left lower penalty area
            self._add_point('l_rupa', l_type, Vector3D( field_half_x - self._penalty_area_dimensions.x,  pa_half_y, 0.0))    # L-junction right upper penalty area
            self._add_point('l_rlpa', l_type, Vector3D( field_half_x - self._penalty_area_dimensions.x, -pa_half_y, 0.0))    # L-junction right lower penalty area
        if has_goalie_area:
            self._add_point('l_luga', l_type, Vector3D(-field_half_x + self._goalie_area_dimensions.x,  ga_half_y, 0.0))     # L-junction left upper goalie area
            self._add_point('l_llga', l_type, Vector3D(-field_half_x + self._goalie_area_dimensions.x, -ga_half_y, 0.0))     # L-junction left lower goalie area
            self._add_point('l_ruga', l_type, Vector3D( field_half_x - self._goalie_area_dimensions.x,  ga_half_y, 0.0))     # L-junction right upper goalie area
            self._add_point('l_rlga', l_type, Vector3D( field_half_x - self._goalie_area_dimensions.x, -ga_half_y, 0.0))     # L-junction right lower goalie area

        l_type = 'x_junction'
        self._add_point('x_cuc', l_type, Vector3D(0.0,  self._middle_circle_radius, 0.0))   # X-junction center upper circle
        self._add_point('x_clc', l_type, Vector3D(0.0, -self._middle_circle_radius, 0.0))   # X-junction center lower circle

        l_type = 'p_junction'
        self._add_point('p_lpm', l_type, Vector3D(-field_half_x + self._penalty_spot_distance, 0.0, 0.0))   # P-junction left penalty mark
        self._add_point('p_rpm', l_type, Vector3D( field_half_x - self._penalty_spot_distance, 0.0, 0.0))   # P-junction right penalty mark

        l_type = 'post'
        self._add_point('g_lup', l_type, Vector3D(-field_half_x,  goal_half_y, 0.0))  # Goal left upper goalpost
        self._add_point('g_llp', l_type, Vector3D(-field_half_x, -goal_half_y, 0.0))  # Goal left lower goalpost
        self._add_point('g_rup', l_type, Vector3D( field_half_x,  goal_half_y, 0.0))  # Goal right upper goalpost
        self._add_point('g_rlp', l_type, Vector3D( field_half_x, -goal_half_y, 0.0))  # Goal right lower goalpost
        # fmt: on


class RCSSField2019(RCSSField2014):
    """Class representing the soccer field used by the RoboCup Humanoid Adult Size in 2019."""

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """Construct a new soccer field description."""

        super().__init__(
            Vector2D(14, 9) if field_dim is None else field_dim,
            goal_dim,
            goalie_area_dim,
            penalty_area_dim,
            1.5 if middle_circle_radius is None else middle_circle_radius,
            2.0 if penalty_spot_distance is None else penalty_spot_distance,
        )


class RCSSField2020(RCSSField2019):
    """Class representing the soccer field used by the RoboCup Humanoid Adult Size since 2020 until now."""

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """Construct a new soccer field description."""

        super().__init__(
            field_dim,
            goal_dim,
            Vector2D(1.0, 4.0) if goalie_area_dim is None else goalie_area_dim,
            Vector2D(3.0, 6.0) if penalty_area_dim is None else penalty_area_dim,
            1.5 if middle_circle_radius is None else middle_circle_radius,
            penalty_spot_distance,
        )
