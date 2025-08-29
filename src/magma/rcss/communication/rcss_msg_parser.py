from __future__ import annotations

from math import radians

from magma.agent.communication.perception import (
    AccelerometerPerceptor,
    GyroRatePerceptor,
    JointStatePerceptor,
    ObjectDetection,
    Perception,
    Pos3DPerceptor,
    PPerceptor,
    Rot3DPerceptor,
    TimePerceptor,
)
from magma.common.communication.sexpression import SExpParser, SExpression
from magma.common.math.geometry.rotation import R3D_IDENTITY, Rotation3D
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D
from magma.rcss.communication.rcss_perception import RCSSGameStatePerceptor, RCSSLineDetection, RCSSPlayerDetection, RCSSVisionPerceptor


class RCSSMessageParser:
    """Parser for MuJoCo Soccer Simulation perception messages."""

    def __init__(self) -> None:
        """Construct a new MuJoCo Soccer Simulation message parser."""

        self._sexp_parser = SExpParser()

    def parse(self, msg: bytes | bytearray) -> Perception:
        """Parse the given message into a list of perceptions.

        Parameter
        ---------
        msg : bytes | bytearray
            The perception message to parse.
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

            elif child[0] == 'HJ':
                # hinge joint perceptor
                perceptor = self._parse_hinge_joint(child)

            elif child[0] == 'GYR':
                # gyro rate perceptor
                perceptor = self._parse_gyro_rate(child)

            elif child[0] == 'ACC':
                # accelerometer perceptor
                perceptor = self._parse_accelerometer(child)

            elif child[0] == 'See':
                # see perceptor
                perceptor = self._parse_vision(child)

            elif child[0] == 'pos':
                # position perceptor
                perceptor = self._parse_pos(child)

            elif child[0] == 'quat':
                # orientation perceptor
                perceptor = self._parse_rot(child)

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
        """Parse a int value."""

        if isinstance(child, SExpression):
            msg = f'Expected string atom: {child}'
            raise TypeError(msg)

        return child

    def _as_int(self, child: str | SExpression) -> int:
        """Parse a int value."""

        if isinstance(child, SExpression):
            msg = f'Expected int atom: {child}'
            raise TypeError(msg)

        return int(child)

    def _as_float(self, child: str | SExpression) -> float:
        """Parse a float value."""

        if isinstance(child, SExpression):
            msg = f'Expected float atom: {child}'
            raise TypeError(msg)

        return float(child)

    def _as_bool(self, child: str | SExpression) -> bool:
        """Parse a bool value."""

        if isinstance(child, SExpression):
            return False

        return child.lower() not in ('false', 'off', 'no', '0')

    def _parse_time(self, node: SExpression) -> TimePerceptor:
        """Parse a time expression.

        Definition: (time (now <float>))
        """

        now_node = node[1]

        if not isinstance(now_node, SExpression):
            # TODO: Raise parser exception
            raise TypeError

        return TimePerceptor(self._as_str(now_node[0]), self._as_float(now_node[1]))

    def _parse_game_state(self, node: SExpression) -> RCSSGameStatePerceptor:
        """Parse a game state expression.

        Definition: (GS (t <play_time>) (pm <play_mode>) (lt <left_team>) (rt <right_team>) (sl <sl>) (sr <sr>))
        """

        play_time: float = 0.0
        left_team_name: str = ''
        right_team_name: str = ''
        play_mode: str = ''
        score_left: int = 0
        score_right: int = 0

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 't':
                play_time = self._as_float(child[1])
            elif child[0] == 'pm':
                play_mode = self._as_str(child[1])
            elif child[0] == 'tl':
                left_team_name = self._as_str(child[1])
            elif child[0] == 'tr':
                right_team_name = self._as_str(child[1])
            elif child[0] == 'sl':
                score_left = self._as_int(child[1])
            elif child[0] == 'sr':
                score_right = self._as_int(child[1])
            else:
                pass

        return RCSSGameStatePerceptor('game_state', play_time, play_mode, left_team_name, right_team_name, score_left, score_right)

    def _parse_hinge_joint(self, node: SExpression) -> JointStatePerceptor:
        """Parse a hinge joint expression.

        Definition: (HJ (name <name>) (ax <ax>) (vx <vx>))
        """

        name: str = ''
        ax: float = 0.0
        vx: float = 0.0

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'name':
                name = self._as_str(child[1])
            elif child[0] == 'ax':
                ax = radians(self._as_float(child[1]))
            elif child[0] == 'vx':
                vx = radians(self._as_float(child[1]))
            else:
                pass

        return JointStatePerceptor(name, ax, vx)

    def _parse_gyro_rate(self, node: SExpression) -> GyroRatePerceptor:
        """Parse a game gyro rate expression.

        Definition: (GYR (name <name>) (rt <rx> <ry> <rz>))
        """

        name: str = ''
        rot: Vector3D = V3D_ZERO

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'name':
                name = self._as_str(child[1])
            elif child[0] == 'rt':
                rot = Vector3D(radians(self._as_float(child[1])), radians(self._as_float(child[2])), radians(self._as_float(child[3])))
            else:
                pass

        return GyroRatePerceptor(name, rot)

    def _parse_accelerometer(self, node: SExpression) -> AccelerometerPerceptor:
        """Parse a accelerometer expression.

        Definition: (ACC (name <name>) (a <ax> <ay> <az>))
        """

        name: str = ''
        acc: Vector3D = V3D_ZERO

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'name':
                name = self._as_str(child[1])
            elif child[0] == 'a':
                acc = Vector3D(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]))
            else:
                pass

        return AccelerometerPerceptor(name, acc)

    def _parse_vision(self, node: SExpression) -> RCSSVisionPerceptor:
        """Parse a vision expression.

        Definition: (See +(<name> (pol <distance> <angle1> <angle2>))
                         +(P (team <teamname>) (id <playerID>) +(<bodypart> (pol <distance> <angle1> <angle2>)))
                         +(L (pol <distance> <angle1> <angle2>) (pol <distance> <angle1> <angle2>)))
        """

        objects: list[ObjectDetection] = []
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

    def _parse_point_object(self, node: SExpression) -> ObjectDetection:
        """Parse a visible object expression.

        Definition: (<name> (pol <angle1> <angle2> <distance>))
        """

        name = self._as_str(node[0])
        pol_node = node[1]

        if not isinstance(pol_node, SExpression):
            msg = f'Expected "pol" expression atom: {pol_node}!'
            raise TypeError(msg)

        return ObjectDetection(name, '', radians(self._as_float(pol_node[1])), radians(self._as_float(pol_node[2])), self._as_float(pol_node[3]))

    def _parse_line_object(self, node: SExpression) -> RCSSLineDetection:
        """Parse a line expression.

        Definition: (L (pol <h-angle> <v-angle> <distance>) (pol <h-angle> <v-angle> <distance>))
        """

        p1_node = node[1]
        p2_node = node[2]

        if not isinstance(p1_node, SExpression) or not isinstance(p2_node, SExpression):
            msg = f'Expected "pol" expression atoms: {p1_node} | {p2_node}!'
            raise TypeError(msg)

        return RCSSLineDetection(self._parse_pol(p1_node), self._parse_pol(p2_node))

    def _parse_player_object(self, node: SExpression) -> RCSSPlayerDetection:
        """Parse a player expression.

        Definition: (P (team <team-name>) (id <player-no>) [(<marker> (pol <h-angle> <v-angle> <distance>))])
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
        """Parse a pol expression into a 3D vector.

        Definition: (pol <azimuth> <inclination> <distance>)
        """

        return Vector3D.from_pol(radians(self._as_float(node[1])), radians(self._as_float(node[2])), self._as_float(node[3]))

    def _parse_pos(self, node: SExpression) -> Pos3DPerceptor:
        """Parse a position expression.

        Definition: (pos (name <name>) (q <qw> <qx> <qy> <qz>))
        """

        name: str = ''
        pos: Vector3D = V3D_ZERO

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'name':
                name = self._as_str(child[1])
            elif child[0] == 'p':
                pos = Vector3D(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]))
            else:
                pass

        return Pos3DPerceptor(name, pos)

    def _parse_rot(self, node: SExpression) -> Rot3DPerceptor:
        """Parse a quaternion expression.

        Definition: (quat (name <name>) (q <qw> <qx> <qy> <qz>))
        """

        name: str = ''
        rot: Rotation3D = R3D_IDENTITY

        for child in node:
            if not isinstance(child, SExpression):
                continue

            if child[0] == 'name':
                name = self._as_str(child[1])
            elif child[0] == 'q':
                rot = Rotation3D.from_quat(self._as_float(child[1]), self._as_float(child[2]), self._as_float(child[3]), self._as_float(child[4]))
            else:
                pass

        return Rot3DPerceptor(name, rot)
