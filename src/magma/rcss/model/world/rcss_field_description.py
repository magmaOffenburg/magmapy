from __future__ import annotations

from enum import Enum

import numpy as np

from magma.common.math.geometry.vector import Vector2D, Vector3D
from magma.soccer_agent.model.world.soccer_field_description import SoccerFieldDescription


class RCSSFieldVersion(Enum):
    """
    Enum specifying the available RoboCup Soccer Simulation league field versions.
    """

    UNKNOWN = 0
    """
    Unknown field version.
    """

    V62 = 62
    """
    Version 62 of the soccer field.
    """

    V63 = 63
    """
    Version 63 of the soccer field.
    """

    V64 = 64
    """
    Version 64 of the soccer field.
    """

    V66 = 66
    """
    Version 66 of the soccer field.
    """

    @staticmethod
    def from_value(version: int | str) -> RCSSFieldVersion:
        """
        Fetch the enum entry corresponding to the given version value.
        """

        version = version if type(version) == 'int' else int(version)

        for v in RCSSFieldVersion:
            if v.value == version:
                return v

        print(f'WARNING: Unknown RCSS field version: "{version}"!')  # noqa: T201

        return RCSSFieldVersion.UNKNOWN

    @staticmethod
    def create_description_for(version: int | str) -> SoccerFieldDescription:
        """
        Create a field description for the given field version.
        """

        version_id = RCSSFieldVersion.from_value(version)

        if version_id == RCSSFieldVersion.V62:
            return RCSSFieldV62()
        if version_id == RCSSFieldVersion.V63:
            return RCSSFieldV63()
        if version_id == RCSSFieldVersion.V64:
            return RCSSFieldV64()

        # cases: V66 and UNKNOWN
        return RCSSFieldV66()


class RCSSFieldV62(SoccerFieldDescription):
    """
    Class representing the soccer field used by the RoboCup Soccer Simulation version 62.
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
            Vector2D(12.0, 8.9) if field_dim is None else field_dim,
            Vector3D(0.4, 1.4, 0.8) if goal_dim is None else goal_dim,
            Vector2D(1.2, 2.6) if goalie_area_dim is None else goalie_area_dim,
            Vector2D() if penalty_area_dim is None else penalty_area_dim,
            1.0 if middle_circle_radius is None else middle_circle_radius,
            0.0 if penalty_spot_distance is None else penalty_spot_distance,
        )

        field_half_length = self._field_dimensions.x() / 2
        field_half_width = self._field_dimensions.y() / 2
        goal_half_width = self._goal_dimensions.y() / 2

        # fmt: off
        # init landmarks
        l_type: str = 'Goalpost'
        self._add_point('G1L', l_type, Vector3D(-field_half_length,  goal_half_width, self._goal_dimensions.z()))  # upper left goal post
        self._add_point('G2L', l_type, Vector3D(-field_half_length, -goal_half_width, self._goal_dimensions.z()))  # lower left goal post
        self._add_point('G1R', l_type, Vector3D( field_half_length,  goal_half_width, self._goal_dimensions.z()))  # upper right goal post
        self._add_point('G2R', l_type, Vector3D( field_half_length, -goal_half_width, self._goal_dimensions.z()))  # lower right goal post

        l_type = 'Flag'
        self._add_point('F1L', l_type, Vector3D(-field_half_length,  field_half_width, 0))  # upper left corner flag
        self._add_point('F2L', l_type, Vector3D(-field_half_length, -field_half_width, 0))  # lower left corner flag
        self._add_point('F1R', l_type, Vector3D( field_half_length,  field_half_width, 0))  # upper right corner flag
        self._add_point('F2R', l_type, Vector3D( field_half_length, -field_half_width, 0))  # lower right corner flag
        # fmt: on


class RCSSFieldV63(RCSSFieldV62):
    """
    Class representing the soccer field used by the RoboCup Soccer Simulation version 63.
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
            Vector2D(18.0, 12.0) if field_dim is None else field_dim,
            Vector3D(0.6, 2.1, 0.8) if goal_dim is None else goal_dim,
            Vector2D(1.8, 3.9) if goalie_area_dim is None else goalie_area_dim,
            penalty_area_dim,
            1.8 if middle_circle_radius is None else middle_circle_radius,
            penalty_spot_distance,
        )


class RCSSFieldV64(RCSSFieldV63):
    """
    Class representing the soccer field used by the RoboCup Soccer Simulation version 64.
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
            Vector2D(21.0, 14.0) if field_dim is None else field_dim,
            goal_dim,
            goalie_area_dim,
            penalty_area_dim,
            middle_circle_radius,
            penalty_spot_distance,
        )

        field_half_length = self._field_dimensions.x() / 2
        field_half_width = self._field_dimensions.y() / 2

        top_left = Vector3D(-field_half_length, field_half_width, 0)
        top_right = Vector3D(field_half_length, field_half_width, 0)
        bottom_left = Vector3D(-field_half_length, -field_half_width, 0)
        bottom_right = Vector3D(field_half_length, -field_half_width, 0)

        # fmt: off
        # init field lines
        l_type = 'FieldLine'
        self._add_line('UGL', l_type, top_left, top_right)        # upper ground line
        self._add_line('LGL', l_type, bottom_left, bottom_right)  # lower ground line

        self._add_line('LSL', l_type, top_left, bottom_left)      # left side line
        self._add_line('RSL', l_type, top_right, bottom_right)    # right side line

        self._add_line('ML', l_type, Vector3D(0, field_half_width, 0), Vector3D(0, -field_half_width, 0))  # middle line

        if self._goalie_area_dimensions.x() > 0 and self._goalie_area_dimensions.y() > 0:
            ga_half_width = self._goalie_area_dimensions.y() / 2
            ga_field_line_x = field_half_length - self._goalie_area_dimensions.x()


            self._add_line('LGAUL', l_type, Vector3D(-field_half_length,  ga_half_width, 0), Vector3D(-ga_field_line_x,  ga_half_width, 0)) # left goalie area upper line
            self._add_line('LGALL', l_type, Vector3D(-field_half_length, -ga_half_width, 0), Vector3D(-ga_field_line_x, -ga_half_width, 0)) # left goalie area lower line
            self._add_line('LGAFL', l_type, Vector3D(  -ga_field_line_x,  ga_half_width, 0), Vector3D(-ga_field_line_x, -ga_half_width, 0)) # left goalie area field line

            self._add_line('RGAUL', l_type, Vector3D(field_half_length,  ga_half_width, 0), Vector3D(ga_field_line_x,  ga_half_width, 0))   # right goalie area upper line
            self._add_line('RGALL', l_type, Vector3D(field_half_length, -ga_half_width, 0), Vector3D(ga_field_line_x, -ga_half_width, 0))   # right goalie area lower line
            self._add_line('RGAFL', l_type, Vector3D(  ga_field_line_x,  ga_half_width, 0), Vector3D(ga_field_line_x, -ga_half_width, 0))   # right goalie area field line

        if self._penalty_area_dimensions.x() > 0 and self._penalty_area_dimensions.y() > 0:
            pa_half_width = self._penalty_area_dimensions.y() / 2
            pa_field_line_x = field_half_length - self._penalty_area_dimensions.x()

            self._add_line('LPAUL', l_type, Vector3D(-field_half_length,  pa_half_width, 0), Vector3D(-pa_field_line_x,  pa_half_width, 0)) # left penalty area upper line
            self._add_line('LPALL', l_type, Vector3D(-field_half_length, -pa_half_width, 0), Vector3D(-pa_field_line_x, -pa_half_width, 0)) # left penalty area lower line
            self._add_line('LPAFL', l_type, Vector3D(  -pa_field_line_x,  pa_half_width, 0), Vector3D(-pa_field_line_x, -pa_half_width, 0)) # left penalty area field line

            self._add_line('RPAUL', l_type, Vector3D(field_half_length,  pa_half_width, 0), Vector3D(pa_field_line_x,  pa_half_width, 0))   # right penalty area upper line
            self._add_line('RPALL', l_type, Vector3D(field_half_length, -pa_half_width, 0), Vector3D(pa_field_line_x, -pa_half_width, 0))   # right penalty area lower line
            self._add_line('RPAFL', l_type, Vector3D(  pa_field_line_x,  pa_half_width, 0), Vector3D(pa_field_line_x, -pa_half_width, 0))   # right penalty area field line
        # fmt: on

        # middle circle lines
        deg_steps = np.arange(0, 361, 36)
        rad_steps = deg_steps * np.pi / 180.0
        pxs = np.cos(rad_steps) * self._middle_circle_radius
        pys = np.sin(rad_steps) * self._middle_circle_radius
        mc_points = [Vector3D(px, py, 0) for px, py in zip(pxs, pys)]

        for i in range(len(mc_points) - 1):
            self._add_line(f'MC_{i}-{deg_steps[i]}', l_type, mc_points[i], mc_points[i + 1])


class RCSSFieldV66(RCSSFieldV64):
    """
    Class representing the soccer field used by the RoboCup Soccer Simulation version 66.
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
            Vector2D(30.0, 20.0) if field_dim is None else field_dim,
            goal_dim,
            goalie_area_dim,
            penalty_area_dim,
            2.0 if middle_circle_radius is None else middle_circle_radius,
            penalty_spot_distance,
        )
