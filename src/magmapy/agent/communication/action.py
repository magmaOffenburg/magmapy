from __future__ import annotations

from collections.abc import ItemsView, Iterator, KeysView, Mapping, Sequence, ValuesView
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, TypeVar, overload

if TYPE_CHECKING:
    from magmapy.common.math.geometry.vector import Vector3D


class PEffector(Protocol):
    """Base protocol for all effectors."""

    @property
    def name(self) -> str:
        """The effector name."""


@dataclass(frozen=True)
class Effector:
    """Base dataclass for effectors."""

    name: str
    """The effector name."""


@dataclass(frozen=True)
class MotorEffector(Effector):
    """Effector for motor actions."""

    position: float
    """The motor target position."""

    velocity: float
    """The motor target velocity."""

    kp: float
    """The motor controller position gain parameter."""

    kd: float
    """The motor controller derivative gain parameter."""

    tau: float
    """The motor torque."""


@dataclass(frozen=True)
class OmniSpeedEffector(Effector):
    """Effector for commanding a desired omni-directional speed towards an external movement platform."""

    desired_speed: Vector3D
    """The desired speed vector."""


class Action(Mapping[str, PEffector]):
    """Map of actions."""

    T = TypeVar('T')

    def __init__(self, actions: Sequence[PEffector] | None = None) -> None:
        """Construct a new action map.

        Parameter
        ---------
        actions : Sequence[PEffector] | None, default=None
            A list of (initial) actions.
        """

        super().__init__()

        self._actions: dict[str, PEffector] = {} if actions is None else {eff.name: eff for eff in actions}

    def put(self, action: PEffector) -> None:
        """Add the given effector to the actions map.

        Parameter
        ---------
        action : PEffector
            The effector to add to the actions map.
        """

        self._actions[action.name] = action

    def get_action(self, name: str, effector_type: type[T]) -> T | None:
        """Retrieve the effector with the given name and type if existing.

        name : str
            The unique name of the effector.

        effector_type: type[T]
            The expected effector type.
        """

        action = self._actions.get(name, None)
        return action if action is not None and isinstance(action, effector_type) else None

    def get_all(self, effector_type: type[T]) -> list[T]:
        """Retrieve the list of effectors with the given type.

        Parameter
        ---------
        effector_type : type[T]
            The effector type to filter.
        """

        return [eff for eff in self._actions.values() if isinstance(eff, effector_type)]

    def items(self) -> ItemsView[str, PEffector]:
        return self._actions.items()

    def keys(self) -> KeysView[str]:
        return self._actions.keys()

    def values(self) -> ValuesView[PEffector]:
        return self._actions.values()

    @overload
    def get(self, key: str, default: PEffector | None = None, /) -> PEffector | None: ...
    @overload
    def get(self, key: str, default: PEffector | T, /) -> PEffector | T: ...
    def get(self, key: str, default: PEffector | T | None = None, /) -> PEffector | T | None:
        return self._actions.get(key, default)

    def __contains__(self, item: object) -> bool:
        return item in self._actions

    def __iter__(self) -> Iterator[str]:
        return self._actions.__iter__()

    def __getitem__(self, key: str) -> PEffector:
        return self._actions[key]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Action):
            return False

        return self._actions == other._actions

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(self._actions)

    def __str__(self) -> str:
        return str(self._actions)
