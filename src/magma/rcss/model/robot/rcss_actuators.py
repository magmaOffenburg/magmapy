from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

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


class PCreateActuator(Protocol):
    """
    Protocol for create actuators.
    """

    def set(self, *, active: bool) -> None:
        """
        Set the create action.
        """

    def get_scene(self) -> str:
        """
        Retrieve the scene path.
        """

    def get_model_type(self) -> int:
        """
        Retrieve the model type number.
        """

    def is_active(self) -> bool:
        """
        Check if the create actuator is active.
        """


class PInitActuator(Protocol):
    """
    Protocol for init actuators.
    """

    def set(self, team_name: str, player_no: int) -> None:
        """
        Set the init action.
        """

    def get_team_name(self) -> str:
        """
        Retrieve the team name.
        """

    def get_player_no(self) -> int:
        """
        Retrieve the player number.
        """

    def is_active(self) -> bool:
        """
        Check if the init actuator is active.
        """


class PSyncActuator(Protocol):
    """
    Protocol for synchronize actuators.
    """

    def set(self, *, active: bool = True) -> None:
        """
        Set the synchronize action.
        """

    def is_active(self) -> bool:
        """
        Check if the synchronize actuator is active.
        """


class PScotty(PActuator, Protocol):
    """
    Protocol for beam actuators.
    """

    def set(self, beam_pose: Pose2D) -> None:
        """
        Set the beam action.
        """

    def get_beam_pose(self) -> Pose2D | None:
        """
        Retrieve the current beam pose.
        """


class PPassModeActuator(PActuator, Protocol):
    """
    Protocol for pass mode actuators.
    """

    def set(self, *, request_pass_mode: bool) -> None:
        """
        Set the pass mode action.
        """

    def is_pass_mode_requested(self) -> bool:
        """
        Retrieve the current pass mode request.
        """


class CreateActuator(Actuator):
    """
    Default create actuator implementation.
    """

    def __init__(
        self,
        name: str,
        effector_name: str,
        scene: str,
        model_type: int,
    ) -> None:
        """
        Create a new create actuator.
        """

        super().__init__(name, effector_name)

        self._scene: str = scene
        self._model_type: int = model_type
        self._active: bool = False

    def set(self, *, active: bool = True) -> None:
        """
        Set the scene action.
        """

        self._active = active

    def get_scene(self) -> str:
        """
        Retrieve the scene path.
        """

        return self._scene

    def get_model_type(self) -> int:
        """
        Retrieve the model type number.
        """

        return self._model_type

    def is_active(self) -> bool:
        """
        Check if the scene actuator is active.
        """

        return self._active

    def commit(self, action: Action) -> None:
        if self._active:
            action.put(CreateEffector(self._effector_name, self._scene, self._model_type))

        # reset actuator
        self._active = False


class InitActuator(Actuator):
    """
    Default init actuator implementation.
    """

    def __init__(self, name: str, effector_name: str) -> None:
        """
        Create a new init actuator.
        """

        super().__init__(name, effector_name)

        self._team_name: str = 'unknown'
        self._player_no: int = 0
        self._active = False

    def set(self, team_name: str, player_no: int) -> None:
        """
        Set the init action.
        """

        self._team_name = team_name
        self._player_no = player_no
        self._active = True

    def get_team_name(self) -> str:
        """
        Retrieve the team name.
        """

        return self._team_name

    def get_player_no(self) -> int:
        """
        Retrieve the player number.
        """

        return self._player_no

    def is_active(self) -> bool:
        """
        Check if the init actuator is active.
        """

        return self._active

    def commit(self, action: Action) -> None:
        if self._active:
            action.put(InitEffector(self._effector_name, self._team_name, self._player_no))

        # reset actuator
        self._active = False


class SyncActuator(Actuator):
    """
    Default synchronize actuator implementation.
    """

    def __init__(
        self,
        name: str,
        effector_name: str,
        *,
        auto_active: bool = True,
    ) -> None:
        """
        Create a new synchronize actuator.
        """

        super().__init__(name, effector_name)

        self._auto_active = auto_active
        self._active = auto_active

    def set(self, *, active: bool = True) -> None:
        """
        Set the synchronize action.
        """

        self._active = active

    def is_active(self) -> bool:
        """
        Check if the synchronize actuator is active.
        """

        return self._active

    def commit(self, action: Action) -> None:
        if self._active:
            action.put(SyncEffector(self._effector_name))

        # reset actuator
        self._active = self._auto_active


class Scotty(Actuator):
    """
    Default beam actuator implementation.
    """

    def __init__(self, name: str, effector_name: str) -> None:
        """
        Create a new beam actuator.
        """

        super().__init__(name, effector_name)

        self._beam_pose: Pose2D | None = None

    def set(self, beam_pose: Pose2D) -> None:
        """
        Set the beam action.
        """

        self._beam_pose = beam_pose

    def get_beam_pose(self) -> Pose2D | None:
        """
        Retrieve the current beam pose.
        """

        return self._beam_pose

    def commit(self, action: Action) -> None:
        if self._beam_pose is not None:
            action.put(BeamEffector(self._effector_name, self._beam_pose))

        # reset actuator
        self._beam_pose = None


class PassModeActuator(Actuator):
    """
    Default pass mode actuator implementation.
    """

    def __init__(self, name: str, effector_name: str) -> None:
        """
        Create a new pass mode actuator.
        """

        super().__init__(name, effector_name)

        self._request_pass_mode: bool = False

    def set(self, *, request_pass_mode: bool = True) -> None:
        """
        Set the pass mode action.
        """

        self._request_pass_mode = request_pass_mode

    def is_pass_mode_requested(self) -> bool:
        """
        Retrieve the current pass mode request.
        """

        return self._request_pass_mode

    def commit(self, action: Action) -> None:
        if self._request_pass_mode:
            action.put(PassModeEffector(self._effector_name))

        # reset actuator
        self._request_pass_mode = False
