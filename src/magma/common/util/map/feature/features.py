from typing import Final, Protocol

from magma.common.math.geometry.vector import Vector3D


class PFeature(Protocol):
    """Base protocol for geometric features."""

    @property
    def name(self) -> str:
        """The unique name of the feature."""

    def get_type(self) -> str:
        """Retrieve the feature type information."""


class PPointFeature(PFeature, Protocol):
    """Point feature with a known fixed position."""

    def get_known_position(self) -> Vector3D:
        """Retrieve the known fixed position of this point feature."""


class PLineFeature(PFeature, Protocol):
    """Line feature, consisting of two known points."""

    def get_known_position1(self) -> Vector3D:
        """Retrieve the first known position of this line feature."""

    def get_known_position2(self) -> Vector3D:
        """Retrieve the first known position of this line feature."""


class GeometricFeature:
    """Base class for geometric features."""

    def __init__(self, name: str, f_type: str) -> None:
        """Construct a new geometric feature.

        Parameter
        ---------
        name : str
            The unique name of the geometric feature.

        f_type : str
            The feature type.
        """

        self.name: Final[str] = name
        """The unique name used to identify the feature."""

        self.f_type: Final[str] = f_type
        """The feature type."""

    def get_type(self) -> str:
        """Retrieve the feature type information."""

        return self.f_type


class PointFeature(GeometricFeature):
    """Default implementation for a point feature with a known position."""

    def __init__(self, name: str, f_type: str, known_pos: Vector3D) -> None:
        """Construct a new point feature.

        Parameter
        ---------
        name : str
            The unique name of the geometric feature.

        f_type : str
            The feature type.

        known_pos : Vector3D
            The known position of the point feature.
        """

        super().__init__(name, f_type)

        self._known_pos: Vector3D = known_pos
        """The known position of this point feature."""

    def get_known_position(self) -> Vector3D:
        """Retrieve the known fixed position of this point feature."""

        return self._known_pos


class LineFeature(GeometricFeature):
    """Default implementation for a line segment feature with a known position."""

    def __init__(
        self,
        name: str,
        f_type: str,
        known_pos1: Vector3D,
        known_pos2: Vector3D,
    ) -> None:
        """Construct a new line segment feature.

        Parameter
        ---------
        name : str
            The unique name of the geometric feature.

        f_type : str
            The feature type.

        known_pos1 : Vector3D
            The first known position of the line segment feature.

        known_pos2 : Vector3D
            The second known position of the line segment feature.
        """

        super().__init__(name, f_type)

        self._known_pos1: Vector3D = known_pos1
        """The first known fixed position of this line segment feature."""

        self._known_pos2: Vector3D = known_pos2
        """The second known fixed position of this line segment feature."""

    def get_known_position1(self) -> Vector3D:
        """Retrieve the first known fixed position of this line segment feature."""

        return self._known_pos1

    def get_known_position2(self) -> Vector3D:
        """Retrieve the second known fixed position of this line segment feature."""

        return self._known_pos2
