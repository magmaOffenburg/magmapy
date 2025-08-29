from math import radians
from typing import Final

from magma.agent.decision.behavior import Behavior
from magma.agent.model.robot.actuators import Motor
from magma.common.math.geometry.angle import angle_to
from magma.soccer_agent.decision.soccer_behaviors import SoccerBehaviorID
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel


class FocusBall(Behavior):
    """The focus ball behavior."""

    def __init__(self, model: PSoccerAgentModel) -> None:
        super().__init__(SoccerBehaviorID.FOCUS_BALL.value)

        self.model: Final[PSoccerAgentModel] = model
        """The agent model."""

        self.head_yaw_motor: Final[Motor | None] = model.get_robot().get_actuator('NeckYaw', Motor)
        """The head yaw axis motor."""

        self.head_pitch_motor: Final[Motor | None] = model.get_robot().get_actuator('NeckPitch', Motor)
        """The head pitch axis motor."""

    def perform(self, *, stop: bool = False) -> None:
        if self.head_yaw_motor is not None and self.head_pitch_motor is not None:
            own_pose = self.model.get_world().get_this_player().get_pose()
            ball_pos = self.model.get_world().get_ball().get_position()
            local_ball_pos = own_pose.inv_tf_vec(ball_pos)

            self.head_yaw_motor.set(angle_to(local_ball_pos).rad(), 0.0, 20, 0.5, 0.0)
            self.head_pitch_motor.set(radians(60), 0.0, 20, 0.5, 0.0)

    def is_finished(self) -> bool:
        return True
