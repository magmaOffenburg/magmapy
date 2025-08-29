from math import ceil

from magma.agent.communication.action import Action, MotorEffector
from magma.rcss.communication.rcss_action import BeamEffector, InitEffector, SyncEffector


class RCSSSMJMessageEncoder:
    """Encoder for RCSSSMJ action messages."""

    def encode(self, action: Action) -> bytes | bytearray:
        """Encode the given action commands into a message.

        Parameter
        ---------
        action : Action
            The action map to encode.
        """

        def round3(val: float) -> float:
            """Round the given float value to 3 digits."""
            return ceil(val * 1000) / 1000.0

        msgs: list[str] = []

        for effector in action.values():
            if isinstance(effector, InitEffector):
                # ignore all other effectors when an init effector is present
                msgs = [f'({effector.name} {effector.model_name} {effector.team_name} {effector.player_no})']
                break

            if isinstance(effector, BeamEffector):
                pose = effector.beam_pose
                msgs.append(f'({effector.name} {round3(pose.x())} {round3(pose.y())} {round3(pose.theta.deg())})')

            elif isinstance(effector, MotorEffector):
                msgs.append(f'({effector.name} {round3(effector.position)} {round3(effector.velocity)} {round3(effector.kp)} {round3(effector.kd)} {round3(effector.tau)})')

            elif isinstance(effector, SyncEffector):
                msgs.append(f'({effector.name})')

        msg = ''.join(msgs)
        # print(msg)
        return msg.encode()
