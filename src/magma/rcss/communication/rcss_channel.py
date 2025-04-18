from __future__ import annotations

from math import cos, radians, sin

from magma.agent.communication.action import Action, MotorEffector
from magma.agent.communication.perception import (
    AccelerometerPerceptor,
    BumperPerceptor,
    GyroRatePerceptor,
    JointStatePerceptor,
    Perception,
    PPerceptor,
    TimePerceptor,
)
from magma.agent.communication.tcp_lpm_channel import TCPLPMChannel
from magma.common.communication.sexpression import SExpParser, SExpression
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D
from magma.rcss.communication.rcss_action import (
    BeamEffector,
    CreateEffector,
    InitEffector,
    PassModeEffector,
    SayEffector,
    SyncEffector,
)
from magma.rcss.communication.rcss_perception import (
    ForceResistancePerceptor,
    RCSSAgentStatePerceptor,
    RCSSHearPerceptor,
    RCSSLineDetection,
    RCSSObjectDetection,
    RCSSPlayerDetection,
    RCSSVisionPerceptor,
)
from magma.soccer_agent.communication.soccer_perception import SoccerGameStatePerceptor


class RCSSMessageParser:
    """
    Parser for RoboCup Soccer Simulation perception messages.
    """

    def __init__(self) -> None:
        """
        Construct a new RoboCup Soccer Simulation message parser.
        """

        self._sexp_parser = SExpParser()

    def parse(self, msg: bytes | bytearray) -> Perception:
        """
        Parse the given message into a list of perceptions.
        """

        perception: Perception = Perception()
        time: float = 0.0

        node: SExpression = self._sexp_parser.parse(msg.decode())

        for child in node:
            # we expect all top level atoms to be symbolic expressions, that contain at least one atom
            # if not isinstance(child, SExpression) or len(child) < 1:
            if not isinstance(child, SExpression) or not child:
                continue

            perceptor: PPerceptor | None = None

            if child[0] == 'time':
                # time perceptor
                perceptor = self._parse_time(child)
                time = perceptor.time

            elif child[0] == 'GS':
                # game state perceptor
                perceptor = self._parse_game_state(child)

            elif child[0] == 'AgentState':
                # agent state perceptor
                perceptor = self._parse_agent_state(child)

            elif child[0] == 'HJ':
                # hinge joint perceptor
                perceptor = self._parse_hinge_joint(child)

            elif child[0] == 'GYR':
                # gyro rate perceptor
                perceptor = self._parse_gyro_rate(child)

            elif child[0] == 'ACC':
                # accelerometer perceptor
                perceptor = self._parse_accelerometer(child)

            elif child[0] == 'TCH':
                # touch perceptor
                perceptor = self._parse_touch(child)

            elif child[0] == 'FRP':
                # force resistance perceptor
                perceptor = self._parse_force_resistance(child)

            elif child[0] == 'See':
                # see perceptor
                perceptor = self._parse_vision(child)

            elif child[0] == 'hear':
                # hear perceptor
                perceptor = self._parse_hear(child)

            else:
                # unknown perceptor
                # print(f"Unknown perceptor: {child[0]}")
                pass

            if perceptor is not None:
                perception.put(perceptor)

        # set perception time
        perception.set_time(time)

        return perception

    def _as_str(self, child: str | SExpression) -> str:
        """
        Parse a int value.
        """

        if isinstance(child, SExpression):
            msg = f'Expected string atom: {child}'
            raise TypeError(msg)

        return child

    def _as_int(self, child: str | SExpression) -> int:
        """
        Parse a int value.
        """

        if isinstance(child, SExpression):
            msg = f'Expected int atom: {child}'
            raise TypeError(msg)

        return int(child)

    def _as_float(self, child: str | SExpression) -> float:
        """
        Parse a float value.
        """

        if isinstance(child, SExpression):
            msg = f'Expected float atom: {child}'
            raise TypeError(msg)

        return float(child)

    def _as_bool(self, child: str | SExpression) -> bool:
        """
        Parse a bool value.
        """

        if isinstance(child, SExpression):
            return False

        return child.lower() not in ('false', 'off', 'no', '0')

    def _parse_time(self, node: SExpression) -> TimePerceptor:
        """
        Parse a time expression.

        Definition: (time (now <float>))
        """

        now_node = node[1]

        if not isinstance(now_node, SExpression):
            # TODO: Raise parser exception
            raise TypeError

        return TimePerceptor(self._as_str(now_node[0]), self._as_float(now_node[1]))

    def _parse_game_state(self, node: SExpression) -> SoccerGameStatePerceptor:
        """
        Parse a game state expression.

        Definition: (GS (sl <sl>) (sr <sr>) (t <play_time>) (pm <play_mode>))
        """

        play_time: float = 0.0
        play_side: str = ''
        play_mode: str = ''
        player_no: int = 0
        score_left: int = 0
        score_right: int = 0

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 't':
                play_time = self._as_float(child[1])
            elif child[0] == 'team':
                play_side = self._as_str(child[1])
            elif child[0] == 'pm':
                play_mode = self._as_str(child[1])
            elif child[0] == 'unum':
                player_no = self._as_int(child[1])
            elif child[0] == 'sl':
                score_left = self._as_int(child[1])
            elif child[0] == 'sr':
                score_right = self._as_int(child[1])
            else:
                pass

        return SoccerGameStatePerceptor('game_state', play_time, play_side, play_mode, player_no, score_left, score_right)

    def _parse_agent_state(self, node: SExpression) -> RCSSAgentStatePerceptor:
        """
        Parse a agent state expression.

        Definition: (AgentState (temp <degree>) (battery <percentile>))
        """

        temperature: int = 0
        battery: int = 0

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'temp':
                temperature = self._as_int(child[1])
            elif child[0] == 'battery':
                battery = self._as_int(child[1])
            else:
                pass

        return RCSSAgentStatePerceptor('agent_state', temperature, battery)

    def _parse_hinge_joint(self, node: SExpression) -> JointStatePerceptor:
        """
        Parse a hinge joint expression.

        Definition: (HJ (n <name>) (ax <ax>))
        """

        name: str = ''
        ax: float = 0.0

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'n':
                name = self._as_str(child[1])
            elif child[0] == 'ax':
                ax = self._as_float(child[1])
            else:
                pass

        return JointStatePerceptor(name, ax)

    def _parse_gyro_rate(self, node: SExpression) -> GyroRatePerceptor:
        """
        Parse a game gyro rate expression.

        Definition: (GYR (n <name>) (rt <rx> <ry> <rz>))
        """

        name: str = ''
        rot: Vector3D = V3D_ZERO

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'n':
                name = self._as_str(child[1])
            elif child[0] == 'rt':
                rot = Vector3D(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]))
            else:
                pass

        return GyroRatePerceptor(name + '_gyro', rot)

    def _parse_accelerometer(self, node: SExpression) -> AccelerometerPerceptor:
        """
        Parse a accelerometer expression.

        Definition: (ACC (n <name>) (a <ax> <ay> <az>))
        """

        name: str = ''
        acc: Vector3D = V3D_ZERO

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'n':
                name = self._as_str(child[1])
            elif child[0] == 'a':
                acc = Vector3D(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]))
            else:
                pass

        return AccelerometerPerceptor(name + '_acc', acc)

    def _parse_touch(self, node: SExpression) -> PPerceptor:
        """
        Parse a touch expression.

        Definition: (TCH n <name> val <bit>)
        """

        return BumperPerceptor(self._as_str(node[2]), active=self._as_bool(node[4]))

    def _parse_force_resistance(self, node: SExpression) -> PPerceptor:
        """
        Parse a force resistance expression.

        Definition: (FRP (n <name>) (c <px> <py> <pz>) (f <fx> <fy> <fz>))
        """

        name: str = ''
        origin: Vector3D = V3D_ZERO
        force: Vector3D = V3D_ZERO

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'n':
                name = self._as_str(child[1])
            elif child[0] == 'c':
                origin = Vector3D(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]))
            elif child[0] == 'f':
                force = Vector3D(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]))
            else:
                pass

        return ForceResistancePerceptor(name, origin, force)

    def _parse_vision(self, node: SExpression) -> RCSSVisionPerceptor:
        """
        Parse a vision expression.

        Definition: (See +(<name> (pol <distance> <angle1> <angle2>))
                         +(P (team <teamname>) (id <playerID>) +(<bodypart> (pol <distance> <angle1> <angle2>)))
                         +(L (pol <distance> <angle1> <angle2>) (pol <distance> <angle1> <angle2>)))
        """

        objects: list[RCSSObjectDetection] = []
        lines: list[RCSSLineDetection] = []
        players: list[RCSSPlayerDetection] = []

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'P':
                players.append(self._parse_player_object(child))
            elif child[0] == 'L':
                lines.append(self._parse_line_object(child))
            else:
                objects.append(self._parse_point_object(child))

        return RCSSVisionPerceptor(self._as_str(node[0]), objects, lines, players)

    def _parse_point_object(self, node: SExpression) -> RCSSObjectDetection:
        """
        Parse a visible object expression.

        Definition: (<name> (pol <distance> <angle1> <angle2>))
        """

        name = self._as_str(node[0])
        pol_node = node[1]

        if not isinstance(pol_node, SExpression):
            msg = f'Expected "pol" expression atom: {pol_node}!'
            raise TypeError(msg)

        return RCSSObjectDetection(name, self._parse_pol(pol_node))

    def _parse_line_object(self, node: SExpression) -> RCSSLineDetection:
        """
        Parse a line expression.

        Definition: (L (pol <distance> <angle1> <angle2>) (pol <distance> <angle1> <angle2>))
        """

        p1_node = node[1]
        p2_node = node[2]

        if not isinstance(p1_node, SExpression) or not isinstance(p2_node, SExpression):
            msg = f'Expected "pol" expression atoms: {p1_node} | {p2_node}!'
            raise TypeError(msg)

        return RCSSLineDetection(self._parse_pol(p1_node), self._parse_pol(p2_node))

    def _parse_player_object(self, node: SExpression) -> RCSSPlayerDetection:
        """
        Parse a player expression.

        Definition: (P (team <teamname>) (id <playerID>) (pol <distance> <angle1> <angle2>)|+(<bodypart> (pol <distance> <angle1> <angle2>)))
        """

        team_name: str = ''
        player_no: int = 0
        body_parts: list[tuple[str, Vector3D]] = []

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'team':
                team_name = self._as_str(child[1])
            elif child[0] == 'id':
                player_no = self._as_int(child[1])
            elif child[0] == 'pol':
                body_parts.append(('torso', self._parse_pol(child)))
            else:
                pol_node = child[1]
                if isinstance(pol_node, SExpression):
                    body_parts.append((self._as_str(child[0]), self._parse_pol(pol_node)))

        return RCSSPlayerDetection(team_name, player_no, body_parts)

    def _parse_pol(self, node: SExpression) -> Vector3D:
        """
        Parse a pol expression into a 3D vector.

        Definition: (pol <distance> <angle1> <angle2>)
        """

        distance: float = self._as_float(node[1])
        alpha: float = radians(self._as_float(node[2]))
        delta: float = radians(self._as_float(node[3]))

        cos_delta = cos(delta)
        x = distance * cos(alpha) * cos_delta
        y = distance * sin(alpha) * cos_delta
        z = distance * sin(delta)

        return Vector3D(x, y, z)

    def _parse_hear(self, node: SExpression) -> RCSSHearPerceptor:
        """
        Parse a head expression.

        Definition: (hear <team> <time> self/<direction> <message>)
        """

        team: str = self._as_str(node[1])
        time: float = self._as_float(node[2])
        direction: str = self._as_str(node[3])
        msg_parts: list[str] = [self._as_str(node[i]) for i in range(4, len(node))]

        return RCSSHearPerceptor(self._as_str(node[0]), time, team, direction, ' '.join(msg_parts))


class RCSSMessageEncoder:
    """
    Encoder for RoboCup Soccer Simulation action messages.
    """

    def encode(self, action: Action) -> bytes | bytearray:
        """
        Encode the given action commands into a message.
        """

        msg: str = ''

        for effector in action.values():
            if isinstance(effector, CreateEffector):
                # ignore all other effectors when a create effector is present
                msg = f'({effector.name} {effector.scene} {effector.model_type})'
                break

            if isinstance(effector, InitEffector):
                # ignore all other effectors when an init effector is present
                msg = f'({effector.name} (unum {effector.player_no}) (teamname {effector.team_name}))'
                break

            if isinstance(effector, BeamEffector):
                pose = effector.beam_pose
                msg += f'({effector.name} {pose.x()} {pose.y()} {pose.theta.deg()})'

            elif isinstance(effector, MotorEffector):
                msg += f'({effector.name} {effector.velocity})'

            elif isinstance(effector, SayEffector):
                msg += f'({effector.name} {effector.message})'

            elif isinstance(effector, (PassModeEffector, SyncEffector)):
                msg += f'({effector.name})'

        return msg.encode()


class RCSSServerChannel(TCPLPMChannel):
    """
    Channel for client communication with the RoboCup Soccer Simulation server.
    """

    def __init__(self, name: str, host: str, port: int = 3100) -> None:
        """
        Construct a new RoboCup soccer simulation server channel.
        """

        super().__init__(name, host, port, RCSSMessageParser(), RCSSMessageEncoder(), 4)
