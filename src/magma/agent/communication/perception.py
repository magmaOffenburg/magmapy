from __future__ import annotations

from collections.abc import ItemsView, Iterator, KeysView, Mapping, Sequence, ValuesView
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, TypeVar, overload

if TYPE_CHECKING:
    from magma.common.math.geometry.pose import Pose3D
    from magma.common.math.geometry.rotation import Rotation3D
    from magma.common.math.geometry.vector import Vector3D


class PPerceptor(Protocol):
    """
    Protocol for all perceptors.
    """

    @property
    def name(self) -> str:
        """
        The perceptor name.
        """


@dataclass(frozen=True)
class Perceptor:
    """
    Base dataclass for perceptors.
    """

    name: str
    """
    The perceptor name.
    """


@dataclass(frozen=True)
class TimePerceptor(Perceptor):
    """
    Perceptor representing a time perception.
    """

    time: float
    """
    The perceived time value.
    """


@dataclass(frozen=True)
class ErrorPerceptor(Perceptor):
    """
    Perceptor representing an communication error.
    """

    severity: str
    """
    The error severity.
    """

    description: str
    """
    A short description of the error.
    """


@dataclass(frozen=True)
class TextPerceptor(Perceptor):
    """
    Perceptor representing a text message.
    """

    text: str
    """
    The perceived text.
    """


@dataclass(frozen=True)
class BumperPerceptor(Perceptor):
    """
    Perceptor representing a simple bumper sensor.
    """

    active: bool
    """
    Perceived bumper activation state.
    True, if the bumper is activated / pressed, False otherwise.
    """


@dataclass(frozen=True)
class GyroRatePerceptor(Perceptor):
    """
    Perceptor representing an 3-dimensional gyroscope sensor.
    """

    rpy: Vector3D
    """
    Perceived angular velocities for roll-pitch-yaw axes.
    """


@dataclass(frozen=True)
class AccelerometerPerceptor(Perceptor):
    """
    Perceptor representing an 3-dimensional accelerometer sensor.
    """

    acceleration: Vector3D
    """
    Perceived linear acceleration.
    """


@dataclass(frozen=True)
class IMUPerceptor(Perceptor):
    """
    Perceptor representing an 3-dimensional IMU sensor.
    """

    orientation: Rotation3D
    """
    Orientation estimation based on gyroscope and accelerometer information.
    """

    acc: Vector3D
    """
    Perceived linear acceleration.
    """

    rpy: Vector3D
    """
    Perceived angular velocities for roll-pitch-yaw axes.
    """


@dataclass(frozen=True)
class JointStatePerceptor(Perceptor):
    """
    Perceptor representing a joint state perception.
    """

    position: float
    """
    The perceived joint position.
    """

    velocity: float = 0.0
    """
    The perceived joint velocity.
    """

    effort: float = 0.0
    """
    The perceived joint motor effort.
    """


@dataclass(frozen=True)
class FreeJointPerceptor(Perceptor):
    """
    Perceptor representing a free joint state perception.
    """

    pose: Pose3D
    """
    The perceived joint pose.
    """


class Perception(Mapping[str, PPerceptor]):
    """
    Map of perceptions.
    """

    T = TypeVar('T')

    def __init__(
        self,
        time: float = 0.0,
        perceptions: Sequence[PPerceptor] | None = None,
        *,
        shutdown: bool = False,
    ) -> None:
        """
        Construct a new perception map.
        """

        super().__init__()

        self._perceptions: dict[str, PPerceptor] = {} if perceptions is None else {p.name: p for p in perceptions}
        self._time: float = time
        self._shutdown: bool = shutdown

    def get_time(self) -> float:
        """
        Retrieve the time of the perception.
        """

        return self._time

    def set_time(self, time: float) -> None:
        """
        Set the time of the perception.
        """

        self._time = time

    def is_shutdown_requested(self) -> bool:
        """
        Flag if the agent perceived a shutdown request.
        """

        return self._shutdown

    def put(self, perceptor: PPerceptor) -> None:
        """
        Add the given perceptor to the perception.
        """

        self._perceptions[perceptor.name] = perceptor

    def get_perceptor(self, name: str, perceptor_type: type[T]) -> T | None:
        """
        Retrieve the perceptor with the given name and type if existing.
        """

        perceptor = self._perceptions.get(name, None)
        return perceptor if perceptor is not None and isinstance(perceptor, perceptor_type) else None

    def get_all(self, perceptor_type: type[T]) -> list[T]:
        """
        Retrieve the list of perceptors with the given type.
        """

        return [p for p in self._perceptions.values() if isinstance(p, perceptor_type)]

    def items(self) -> ItemsView[str, PPerceptor]:
        return self._perceptions.items()

    def keys(self) -> KeysView[str]:
        return self._perceptions.keys()

    def values(self) -> ValuesView[PPerceptor]:
        return self._perceptions.values()

    @overload
    def get(self, key: str, default: PPerceptor | None = None, /) -> PPerceptor | None: ...
    @overload
    def get(self, key: str, default: PPerceptor | T, /) -> PPerceptor | T: ...
    def get(self, key: str, default: PPerceptor | T | None = None, /) -> PPerceptor | T | None:
        return self._perceptions.get(key, default)

    def __contains__(self, item: object) -> bool:
        return item in self._perceptions

    def __iter__(self) -> Iterator[str]:
        return self._perceptions.__iter__()

    def __getitem__(self, key: str) -> PPerceptor:
        return self._perceptions[key]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Perception):
            return False

        return self._time == other._time and self._shutdown == other._shutdown and self._perceptions == other._perceptions

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(self._perceptions)

    def __str__(self) -> str:
        return str(self._perceptions)
