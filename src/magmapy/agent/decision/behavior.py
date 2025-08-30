from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from magmapy.common.math.geometry.vector import Vector3D


class BehaviorID(Enum):
    """Enum specifying behavior names."""

    NONE = 'none'
    """The none behavior used to do nothing."""

    INIT = 'init'
    """The init behavior used to initialize a robot."""

    GET_READY = 'get_ready'
    """The get-ready behavior used bring the robot into a predefined save ready state / posture."""

    MOVE = 'move'
    """The move behavior used to move a robot."""


@runtime_checkable
class PBehavior(Protocol):
    """Base protocol for behaviors."""

    @property
    def name(self) -> str:
        """The unique name of the behavior."""

    def perform(self, *, stop: bool = False) -> None:
        """Perform the next step of this behavior.

        Parameter
        ---------
        stop : bool, default=False
            Flag indicating that the behavior execution is intended to stop (required for cyclic behaviors like walk, etc.).
        """

    def is_finished(self) -> bool:
        """Check if the behavior is finished."""

    def init(self) -> None:
        """(Re-)initialize the state machine of the behavior (if existing)."""

    def abort(self) -> None:
        """Abort this behavior (hard stop)."""

    def switch_from(self, actual_behavior: PBehavior) -> PBehavior:
        """Try switching from the currently active behavior to this behavior.

        Parameter
        ---------
        actual_behavior : PBehavior
            The currently active behavior.

        Returns
        -------
        behavior : PBehavior
            Self, if it is possible to switch to this behavior, otherwise the currently active behavior is returned.
        """

    def on_leaving_behavior(self, new_behavior: PBehavior) -> None:
        """Notify this behavior that it is no longer performed and replaced by the new behavior.

        Parameter
        ---------
        new_behavior : PBehavior
            The new behavior, which will replace this behavior.
        """


@runtime_checkable
class PComplexBehavior(PBehavior, Protocol):
    """Base protocol for complex behaviors."""

    def get_current_behavior(self) -> PBehavior:
        """Return the currently active behavior."""


@runtime_checkable
class PMoveBehavior(PBehavior, Protocol):
    """Protocol for move behaviors."""

    def set(self, desired_speed: Vector3D) -> None:
        """Set the desired movement speed.

        Parameter
        ---------
        desired_speed : Vector3D
            The desired movement speed vector (x, y, theta).
        """


class Behavior(ABC):
    """The behavior class for representing agent action threads."""

    def __init__(self, name: str) -> None:
        """Construct a new behavior.

        Parameter
        ---------
        name : str
            The unique name of the behavior.
        """

        self.name: Final[str] = name
        """The unique name of the behavior."""

    @abstractmethod
    def perform(self, *, stop: bool = False) -> None:
        """Perform the next step of this behavior.

        Parameter
        ---------
        stop : bool, default=False
            Flag indicating that the behavior execution is intended to stop (required for cyclic behaviors like walk, etc.).
        """

    @abstractmethod
    def is_finished(self) -> bool:
        """Check if the behavior is finished."""

    def init(self) -> None:
        """(Re-)initialize the state machine of the behavior (if existing)."""

    def abort(self) -> None:
        """Abort this behavior (hard stop)."""

        self.init()

    def switch_from(self, actual_behavior: PBehavior) -> PBehavior:
        """Try switching from the currently active behavior to this behavior.

        Parameter
        ---------
        actual_behavior : PBehavior
            The currently active behavior.

        Returns
        -------
        behavior : PBehavior
            Self, if it is possible to switch to this behavior, otherwise the currently active behavior is returned.
        """

        if actual_behavior.is_finished():
            actual_behavior.on_leaving_behavior(self)
            return self

        return actual_behavior

    def on_leaving_behavior(self, new_behavior: PBehavior) -> None:
        """Notify this behavior that it is no longer performed and replaced by the new behavior.

        Parameter
        ---------
        new_behavior : PBehavior
            The new behavior, which will replace this behavior.
        """

        if new_behavior != self:
            self.init()


class ComplexBehavior(Behavior):
    """Base class for complex behaviors."""

    def __init__(self, name: str, behaviors: Mapping[str, PBehavior]) -> None:
        """Construct a new complex behavior.

        Parameter
        ---------
        name : str
            The unique name of the behavior.

        behaviors : dict[str, PBehavior]
            The map of known behaviors.
        """

        super().__init__(name)

        self.behaviors: Final[Mapping[str, PBehavior]] = behaviors
        """The map of known behaviors."""

        self._current_behavior: PBehavior = behaviors[BehaviorID.NONE.value]
        """The currently active sub behavior."""

    def get_current_behavior(self) -> PBehavior:
        """Return the currently active behavior."""

        return self._current_behavior

    @abstractmethod
    def _decide(self) -> Sequence[PBehavior]:
        """Decide for a list of possible sub behaviors, sorted from the most to the least preferred behavior."""

    def perform(self, *, stop: bool = False) -> None:
        if not stop:
            # decide which sub behavior(s) to perform next
            desired_behaviors = self._decide()

            if not desired_behaviors:
                # if no explicit decision is made default to the NONE behavior
                desired_behaviors = (self.behaviors[BehaviorID.NONE.value],)

            for behavior in desired_behaviors:
                # check if desired behavior is already active
                if behavior == self._current_behavior:
                    stop = False
                    break

                # try to switch to the desired behavior
                next_behavior = behavior.switch_from(self._current_behavior)
                if next_behavior != self._current_behavior:
                    # behavior switch was successful
                    self._current_behavior = next_behavior
                    stop = False
                    break

                # signal switch intention
                stop = True

        # forward call to current behavior
        self._current_behavior.perform(stop=stop)

    def is_finished(self) -> bool:
        return self._current_behavior.is_finished()

    def init(self) -> None:
        super().init()

        # We have to reset the current behavior.
        # Otherwise, on the next invocation of this complex behavior, the old "current behavior" will be asked if is is finished, which doesn't make much sense.
        self._current_behavior = self.behaviors[BehaviorID.NONE.value]

    def abort(self) -> None:
        self._current_behavior.abort()
        super().abort()

    def switch_from(self, actual_behavior: PBehavior) -> PBehavior:
        # decide which sub behavior(s) to perform next
        desired_behaviors = self._decide()

        if not desired_behaviors:
            # if no explicit decision is made default to the NONE behavior
            desired_behaviors = (self.behaviors[BehaviorID.NONE.value],)

        for behavior in desired_behaviors:
            # if the desired behavior is already in execution, directly switch to this behavior
            if is_behavior_in_execution(behavior, actual_behavior):
                if actual_behavior != behavior:
                    actual_behavior.on_leaving_behavior(behavior)

                # initialize this complex behavior
                self._current_behavior = behavior
                return self

            # if the desired behavior is not already in execution, try to switch to it
            if behavior == behavior.switch_from(actual_behavior):
                self._current_behavior = behavior
                return self

        return actual_behavior

    def on_leaving_behavior(self, new_behavior: PBehavior) -> None:
        if new_behavior == self:
            return

        if self._current_behavior != new_behavior:
            self._current_behavior.on_leaving_behavior(new_behavior)

        super().on_leaving_behavior(new_behavior)


class SingleComplexBehavior(ComplexBehavior):
    """Base class for complex behaviors that decide for a single sub behavior."""

    def __init__(self, name: str, behaviors: Mapping[str, PBehavior]) -> None:
        """Construct a new complex behavior.

        Parameter
        ---------
        name : str
            The unique name of the behavior.

        behaviors : dict[str, PBehavior]
            The map of known behaviors.
        """

        super().__init__(name, behaviors)

    def _decide(self) -> Sequence[PBehavior]:
        """Decide for a list of possible sub behaviors, sorted from the most to the least preferred behavior."""

        desired_behavior = self._decide_next()

        return (self.behaviors[BehaviorID.NONE.value],) if desired_behavior is None else (desired_behavior,)

    @abstractmethod
    def _decide_next(self) -> PBehavior | None:
        """Decide for the next sub behavior to perform."""


def is_behavior_in_execution(testee: PBehavior, reference: PBehavior) -> bool:
    """Check if the testee behavior is in execution by the reference behavior.

    Parameter
    ---------
    testee : PBehavior
        The behavior we are looking for.

    reference : PBehavior
        The reference behavior in which to search for the testee
    """

    ref = reference

    while ref is not None and isinstance(ref, ComplexBehavior):
        if testee == ref:
            return True

        ref = ref.get_current_behavior()

    return testee == ref


def get_behavior_chain(reference: PBehavior) -> Sequence[PBehavior]:
    """Collect the chain of behaviors in execution by the given reference behavior.

    Parameter
    ---------
    reference : PBehavior
        The top-level behavior to expand.
    """

    chain: list[PBehavior] = []
    ref = reference

    # traverse down the chain of complex behaviors
    while ref is not None and isinstance(ref, ComplexBehavior):
        chain.append(ref)

        ref = ref.get_current_behavior()

    # append the final basic behavior
    if ref is not None:
        chain.append(ref)

    return chain
