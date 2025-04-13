from __future__ import annotations

from enum import Enum

from magma.common.math.geometry.vector import Vector2D, Vector3D
from magma.soccer_agent.model.world.soccer_field_description import SoccerFieldDescription


class RCHLFieldVersion(Enum):
    """
    Enum specifying the available RoboCup Humanoid Soccer league field versions.
    """

    UNKNOWN = 'unknown'
    """
    Unknown field version.
    """

    ADULT_2014 = 'hl_adult_2014'
    """
    2014 version of the Adult Size soccer field.
    """

    ADULT_2017 = 'hl_adult_2017'
    """
    2017 version of the Adult Size soccer field.
    """

    ADULT_2019 = 'hl_adult_2019'
    """
    2019 version of the Adult Size soccer field.
    """

    ADULT_2021 = 'hl_adult_2021'
    """
    2021 version of the Adult Size soccer field.
    """

    @staticmethod
    def from_value(version: str) -> RCHLFieldVersion:
        """
        Fetch the enum entry corresponding to the given version value.
        """

        for v in RCHLFieldVersion:
            if v.value == version:
                return v

        print(f'WARNING: Unknown HL field version: "{version}"!')  # noqa: T201

        return RCHLFieldVersion.UNKNOWN

    @staticmethod
    def create_description_for(version: str) -> SoccerFieldDescription:
        """
        Create a field description for the given field version.
        """

        version_id = RCHLFieldVersion.from_value(version)

        if version_id == RCHLFieldVersion.ADULT_2014:
            return RCHLAdultField2014()
        if version_id == RCHLFieldVersion.ADULT_2017:
            return RCHLAdultField2017()
        if version_id == RCHLFieldVersion.ADULT_2019:
            return RCHLAdultField2019()

        # cases: ADULT_2021 and UNKNOWN
        return RCHLAdultField2021()


class RCHLAdultField2014(SoccerFieldDescription):
    """
    Class representing the soccer field used by the RoboCup Humanoid Adult Size in 2014, 2015 and 2016.
    """

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """
        Construct a new soccer field description.
        """

        super().__init__(
            Vector2D(9.0, 6.0) if field_dim is None else field_dim,
            Vector3D(0.6, 2.6, 1.8) if goal_dim is None else goal_dim,
            Vector2D(1.0, 5.0) if goalie_area_dim is None else goalie_area_dim,
            Vector2D() if penalty_area_dim is None else penalty_area_dim,
            0.75 if middle_circle_radius is None else middle_circle_radius,
            2.1 if penalty_spot_distance is None else penalty_spot_distance,
        )

        field_half_x = self._field_dimensions.x() / 2
        field_half_y = self._field_dimensions.y() / 2
        goal_half_y = self._goal_dimensions.y() / 2
        ga_half_y = self._goalie_area_dimensions.y() / 2
        pa_half_y = self._penalty_area_dimensions.y() / 2

        has_goalie_area = self._goalie_area_dimensions.x() > 0 and self._goalie_area_dimensions.y() > 0
        has_penalty_area = self._penalty_area_dimensions.x() > 0 and self._penalty_area_dimensions.y() > 0

        # fmt: off
        # init landmarks
        l_type = 't_junction'
        self._add_point('t_clf', l_type, Vector3D(0.0,  field_half_y, 0.0))   # T-junction center left field
        self._add_point('t_crf', l_type, Vector3D(0.0, -field_half_y, 0.0))   # T-junction center right field
        if has_penalty_area:
            self._add_point('t_slpa', l_type, Vector3D(-field_half_x,  pa_half_y, 0.0))   # T-junction self left penalty area
            self._add_point('t_srpa', l_type, Vector3D(-field_half_x, -pa_half_y, 0.0))   # T-junction self right penalty area
            self._add_point('t_olpa', l_type, Vector3D( field_half_x,  pa_half_y, 0.0))   # T-junction other left penalty area
            self._add_point('t_orpa', l_type, Vector3D( field_half_x, -pa_half_y, 0.0))   # T-junction other right penalty area
        if has_goalie_area:
            self._add_point('t_slga', l_type, Vector3D(-field_half_x,  ga_half_y, 0.0))   # T-junction self left goalie area
            self._add_point('t_srga', l_type, Vector3D(-field_half_x, -ga_half_y, 0.0))   # T-junction self right goalie area
            self._add_point('t_olga', l_type, Vector3D( field_half_x,  ga_half_y, 0.0))   # T-junction other left goalie area
            self._add_point('t_orga', l_type, Vector3D( field_half_x, -ga_half_y, 0.0))   # T-junction other right goalie area

        l_type = 'l_junction'
        self._add_point('l_slf', l_type, Vector3D(-field_half_x,  field_half_y, 0.0))     # L-junction self left field
        self._add_point('l_srf', l_type, Vector3D(-field_half_x, -field_half_y, 0.0))     # L-junction self right field
        self._add_point('l_olf', l_type, Vector3D( field_half_x,  field_half_y, 0.0))     # L-junction other left field
        self._add_point('l_orf', l_type, Vector3D( field_half_x, -field_half_y, 0.0))     # L-junction other right field
        if has_penalty_area:
            self._add_point('l_slpa', l_type, Vector3D(-field_half_x + self._penalty_area_dimensions.x(),  pa_half_y, 0.0))    # L-junction self left penalty area
            self._add_point('l_srpa', l_type, Vector3D(-field_half_x + self._penalty_area_dimensions.x(), -pa_half_y, 0.0))    # L-junction self right penalty area
            self._add_point('l_olpa', l_type, Vector3D( field_half_x - self._penalty_area_dimensions.x(),  pa_half_y, 0.0))    # L-junction other left penalty area
            self._add_point('l_orpa', l_type, Vector3D( field_half_x - self._penalty_area_dimensions.x(), -pa_half_y, 0.0))    # L-junction other right penalty area
        if has_goalie_area:
            self._add_point('l_slga', l_type, Vector3D(-field_half_x + self._goalie_area_dimensions.x(),  ga_half_y, 0.0))     # L-junction self left goalie area
            self._add_point('l_srga', l_type, Vector3D(-field_half_x + self._goalie_area_dimensions.x(), -ga_half_y, 0.0))     # L-junction self right goalie area
            self._add_point('l_olga', l_type, Vector3D( field_half_x - self._goalie_area_dimensions.x(),  ga_half_y, 0.0))     # L-junction other left goalie area
            self._add_point('l_orga', l_type, Vector3D( field_half_x - self._goalie_area_dimensions.x(), -ga_half_y, 0.0))     # L-junction other right goalie area

        l_type = 'x_junction'
        self._add_point('x_clc', l_type, Vector3D(0.0,  self._middle_circle_radius, 0.0))   # X-junction center left circle
        self._add_point('x_crc', l_type, Vector3D(0.0, -self._middle_circle_radius, 0.0))   # X-junction center right circle

        l_type = 'p_junction'
        self._add_point('p_smx', l_type, Vector3D(-field_half_x + self._penalty_spot_distance, 0.0, 0.0))   # L-junction self left penalty area
        self._add_point('p_omx', l_type, Vector3D( field_half_x - self._penalty_spot_distance, 0.0, 0.0))   # L-junction self left penalty area

        l_type = 'post'
        self._add_point('g_srg', l_type, Vector3D(-field_half_x, -goal_half_y, 0.0))  # Goal self right goalpost
        self._add_point('g_slg', l_type, Vector3D(-field_half_x,  goal_half_y, 0.0))  # Goal self left goalpost
        self._add_point('g_org', l_type, Vector3D( field_half_x, -goal_half_y, 0.0))  # Goal other right goalpost
        self._add_point('g_olg', l_type, Vector3D( field_half_x,  goal_half_y, 0.0))  # Goal other left goalpost
        # fmt: on


class RCHLAdultField2017(RCHLAdultField2014):
    """
    Class representing the soccer field used by the RoboCup Humanoid Adult Size in 2017 and 2018.
    """

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """
        Construct a new soccer field description.
        """

        super().__init__(
            field_dim,
            Vector3D(0.6, 2.6, 1.8) if goal_dim is None else goal_dim,
            goalie_area_dim,
            penalty_area_dim,
            middle_circle_radius,
            penalty_spot_distance,
        )


class RCHLAdultField2019(RCHLAdultField2017):
    """
    Class representing the soccer field used by the RoboCup Humanoid Adult Size in 2019 and 2020.
    """

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """
        Construct a new soccer field description.
        """

        super().__init__(
            Vector2D(14, 9) if field_dim is None else field_dim,
            goal_dim,
            goalie_area_dim,
            penalty_area_dim,
            1.5 if middle_circle_radius is None else middle_circle_radius,
            2.0 if penalty_spot_distance is None else penalty_spot_distance,
        )


class RCHLAdultField2021(RCHLAdultField2019):
    """
    Class representing the soccer field used by the RoboCup Humanoid Adult Size since 2021 until now.
    """

    def __init__(
        self,
        field_dim: Vector2D | None = None,
        goal_dim: Vector3D | None = None,
        goalie_area_dim: Vector2D | None = None,
        penalty_area_dim: Vector2D | None = None,
        middle_circle_radius: float | None = None,
        penalty_spot_distance: float | None = None,
    ) -> None:
        """
        Construct a new soccer field description.
        """

        super().__init__(
            field_dim,
            goal_dim,
            Vector2D(1.0, 4.0) if goalie_area_dim is None else goalie_area_dim,
            Vector2D(3.0, 6.0) if penalty_area_dim is None else penalty_area_dim,
            1.5 if middle_circle_radius is None else middle_circle_radius,
            penalty_spot_distance,
        )
