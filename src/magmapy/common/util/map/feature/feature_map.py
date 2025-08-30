from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

    from magmapy.common.util.map.feature.features import PLineFeature, PPointFeature


class PFeatureMap(Protocol):
    """
    A map of known fixed geometric features.
    """

    def get_point_features(self) -> Sequence[PPointFeature]:
        """
        Retrieve the collection of known point features.
        """

    def get_line_features(self) -> Sequence[PLineFeature]:
        """
        Retrieve the collection of known line features.
        """


class PMutableFeatureMap(PFeatureMap, Protocol):
    """
    A mutable map of known fixed geometric features.
    """

    def set_point_features(self, features: Sequence[PPointFeature]) -> None:
        """
        Set the collection of known point features.
        """

    def set_line_features(self, features: Sequence[PLineFeature]) -> None:
        """
        Set the collection of known line features.
        """


class FeatureMap:
    """
    Default implementation of a feature map.
    """

    def __init__(
        self,
        point_features: Sequence[PPointFeature] | None = None,
        line_features: Sequence[PLineFeature] | None = None,
    ) -> None:
        """
        Construct a new feature map.
        """

        self._point_features: Sequence[PPointFeature] = () if point_features is None else point_features
        self._line_features: Sequence[PLineFeature] = () if line_features is None else line_features

    def get_point_features(self) -> Sequence[PPointFeature]:
        """
        Retrieve the collection of known point features.
        """

        return self._point_features

    def set_point_features(self, features: Sequence[PPointFeature]) -> None:
        """
        Set the collection of known point features.
        """

        self._point_features = features

    def get_line_features(self) -> Sequence[PLineFeature]:
        """
        Retrieve the collection of known line features.
        """

        return self._line_features

    def set_line_features(self, features: Sequence[PLineFeature]) -> None:
        """
        Set the collection of known line features.
        """

        self._line_features = features
