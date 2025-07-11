from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol, runtime_checkable

from magma.agent.model.robot.actuators import Actuator, PActuator
from magma.rcss.communication.rcss_action import (
    BeamEffector,
    CreateEffector,
    InitEffector,
    PassModeEffector,
    SyncEffector,
)

if TYPE_CHECKING:
    from magma.agent.communication.action import Action
    from magma.common.math.geometry.pose import Pose2D


@runtime_checkable
class PCreateActuator(Protocol):
    """Protocol for create actuators."""

    def set(self, *, active: bool) -> None:
        """Set the create action.

        Parameter
        ---------
        active : bool
            Enable / disable create actuator.
        """

    @property
    def scene(self) -> str:
        """The scene path."""

    @property
    def model_type(self) -> int:
        """Retrieve the model type number."""

    def is_active(self) -> bool:
        """Check if the create actuator is active."""


@runtime_checkable
class PInitActuator(Protocol):
    """Protocol for init actuators."""

    def set(self, team_name: str, player_no: int) -> None:
        """Set the init action.

        Parameter
        ---------
        team_name : str
            The name of the team this agent belongs to.

        player_no : int
            The player number of this agent.
        """

    def get_team_name(self) -> str:
        """Retrieve the team name."""

    def get_player_no(self) -> int:
        """Retrieve the player number."""

    def is_active(self) -> bool:
        """Check if the init actuator is active."""


@runtime_checkable
class PSyncActuator(Protocol):
    """Protocol for synchronize actuators."""

    def set(self, *, active: bool = True) -> None:
        """Set the synchronize action.

        Parameter
        ---------
        active : bool
            Enable / disable sync actuator.
        """

    def is_active(self) -> bool:
        """Check if the synchronize actuator is active."""


@runtime_checkable
class PScotty(PActuator, Protocol):
    """Protocol for beam actuators."""

    def set(self, beam_pose: Pose2D) -> None:
        """Set the beam action.

        Parameter
        ---------
        beam_pose : Pose2D
            The beam target pose (x, y, theta).
        """

    def get_beam_pose(self) -> Pose2D | None:
        """Retrieve the current beam pose."""


@runtime_checkable
class PPassModeActuator(PActuator, Protocol):
    """Protocol for pass mode actuators."""

    def set(self, *, request_pass_mode: bool) -> None:
        """Set the pass mode action.

        Parameter
        ---------
        request_pass_mode : bool
            Enable / disable pass mode.
        """

    def is_pass_mode_requested(self) -> bool:
        """Retrieve the current pass mode request."""


class CreateActuator(Actuator):
    """Default create actuator implementation."""

    def __init__(
        self,
        name: str,
        effector_name: str,
        scene: str,
        model_type: int,
    ) -> None:
        """Create a new create actuator.

        Parameter
        ---------
        name : str
            The unique actuator name.

        effector_name : str
            The name of the effector associated with this actuator.

        scene : str
            The robot model scene path.

        model_type : int
            The model type variant.
        """

        super().__init__(name, effector_name)

        self.scene: Final[str] = scene
        """The robot model scene path."""

        self.model_type: Final[int] = model_type
        """The model type variant."""

        self._active: bool = False
        """Flag indicating if this actuator is active or not."""

    def set(self, *, active: bool = True) -> None:
        """Set the scene action.

        Parameter
        ---------
        active : bool
            Enable / disable create actuator.
        """

        self._active = active

    def is_active(self) -> bool:
        """Check if the scene actuator is active."""

        return self._active

    def commit(self, action: Action) -> None:
        if self._active:
            action.put(CreateEffector(self.effector_name, self.scene, self.model_type))

        # reset actuator
        self._active = False


class InitActuator(Actuator):
    """Default init actuator implementation."""

    def __init__(self, name: str, effector_name: str, model_name: str = '') -> None:
        """Create a new init actuator.

        Parameter
        ---------
        name : str
            The unique actuator name.

        effector_name : str
            The name of the effector associated with this actuator.

        model_name : str, default=''
            The name of the robot model to use.
        """

        super().__init__(name, effector_name)

        self._model_name: Final[str] = model_name
        """The robot model name."""

        self._team_name: str = 'unknown'
        """THe name of the team this agent belongs to."""

        self._player_no: int = 0
        """The player number of the agent."""

        self._active: bool = False
        """Flag indicating if this actuator is active or not."""

    def set(self, team_name: str, player_no: int) -> None:
        """Set the init action.

        Parameter
        ---------
        team_name : str
            The name of the team this agent belongs to.

        player_no : int
            The player number of this agent.
        """

        self._team_name = team_name
        self._player_no = player_no
        self._active = True

    def get_model_name(self) -> str:
        """Retrieve the robot model name."""

        return self._team_name

    def get_team_name(self) -> str:
        """Retrieve the team name."""

        return self._team_name

    def get_player_no(self) -> int:
        """Retrieve the player number."""

        return self._player_no

    def is_active(self) -> bool:
        """Check if the init actuator is active."""

        return self._active

    def commit(self, action: Action) -> None:
        if self._active:
            action.put(InitEffector(self.effector_name, self._team_name, self._player_no, self._model_name))

        # reset actuator
        self._active = False


class SyncActuator(Actuator):
    """Default synchronize actuator implementation."""

    def __init__(
        self,
        name: str,
        effector_name: str,
        *,
        auto_active: bool = True,
    ) -> None:
        """Create a new synchronize actuator.

        Parameter
        ---------
        name : str
            The unique actuator name.

        effector_name : str
            The name of the effector associated with this actuator.

        auto_active : bool = True
            Automatically reactivate the actuator each cycle.
        """

        super().__init__(name, effector_name)

        self.auto_active: Final[bool] = auto_active
        """Flag indicating if this actuator is automatically reactivated after committing an action."""

        self._active: bool = auto_active
        """Flag indicating if this actuator is active or not."""

    def set(self, *, active: bool = True) -> None:
        """Set the synchronize action.

        Parameter
        ---------
        active : bool
            Enable / disable sync actuator.
        """

        self._active = active

    def is_active(self) -> bool:
        """Check if the synchronize actuator is active."""

        return self._active

    def commit(self, action: Action) -> None:
        if self._active:
            action.put(SyncEffector(self.effector_name))

        # reset actuator
        self._active = self.auto_active


class Scotty(Actuator):
    """Default beam actuator implementation."""

    def __init__(self, name: str, effector_name: str) -> None:
        """Create a new beam actuator.

        Parameter
        ---------
        name : str
            The unique actuator name.

        effector_name : str
            The name of the effector associated with this actuator.
        """

        super().__init__(name, effector_name)

        self._beam_pose: Pose2D | None = None
        """The target beam pose (if existing)."""

    def set(self, beam_pose: Pose2D) -> None:
        """Set the beam action.

        Parameter
        ---------
        beam_pose : Pose2D
            The beam target pose (x, y, theta).
        """

        self._beam_pose = beam_pose

    def get_beam_pose(self) -> Pose2D | None:
        """Retrieve the current beam pose."""

        return self._beam_pose

    def commit(self, action: Action) -> None:
        if self._beam_pose is not None:
            action.put(BeamEffector(self.effector_name, self._beam_pose))

        # reset actuator
        self._beam_pose = None


class PassModeActuator(Actuator):
    """Default pass mode actuator implementation."""

    def __init__(self, name: str, effector_name: str) -> None:
        """Create a new pass mode actuator.

        Parameter
        ---------
        name : str
            The unique actuator name.

        effector_name : str
            The name of the effector associated with this actuator.
        """

        super().__init__(name, effector_name)

        self._request_pass_mode: bool = False
        """Flag indicating if pass-mode should be requested."""

    def set(self, *, request_pass_mode: bool = True) -> None:
        """Set the pass mode action.

        Parameter
        ---------
        request_pass_mode : bool
            Enable / disable pass mode.
        """

        self._request_pass_mode = request_pass_mode

    def is_pass_mode_requested(self) -> bool:
        """Retrieve the current pass mode request."""

        return self._request_pass_mode

    def commit(self, action: Action) -> None:
        if self._request_pass_mode:
            action.put(PassModeEffector(self.effector_name))

        # reset actuator
        self._request_pass_mode = False
