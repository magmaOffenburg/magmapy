from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import pi, sin

from magma.agent.model.robot.robot_description import (
    AccelerometerDescription,
    ActuatorDescription,
    BodyDescription,
    CameraDescription,
    FixedJointDescription,
    GyroDescription,
    HingeJointDescription,
    InertiaDescription,
    MotorDescription,
    RobotDescription,
    SensorDescription,
    VisualDescription,
)
from magma.common.math.geometry.vector import V3D_UNIT_NEG_Y, V3D_UNIT_X, V3D_UNIT_Y, V3D_UNIT_Z


class RCSSRobots(Enum):
    """
    Enum specifying the available RoboCup Soccer Simulation league robot models.
    """

    UNKNOWN = 'unknown'
    """
    Unknown robot model.
    """

    NAO = 'Nao'
    """
    The default Nao robot model.
    """

    NAO0 = 'Nao0'
    """
    Type variant 0 of the Nao-Hetero robot model.
    """

    NAO1 = 'Nao1'
    """
    Type variant 1 of the Nao-Hetero robot model.
    """

    NAO2 = 'Nao2'
    """
    Type variant 2 of the Nao-Hetero robot model.
    """

    NAO3 = 'Nao3'
    """
    Type variant 3 of the Nao-Hetero robot model.
    """

    NAO4 = 'Nao4'
    """
    Type variant 4 of the Nao-Hetero robot model.
    """

    NAO_TOE = 'NaoToe'
    """
    Synonym for type variant 4 of the Nao robot model.
    """

    @staticmethod
    def from_value(name: str) -> RCSSRobots:
        """
        Fetch the enum entry corresponding to the given name value.
        """

        for v in RCSSRobots:
            if v.value == name:
                return v

        print(f'WARNING: Unknown RCSS robot model: "{name}"!')  # noqa: T201

        return RCSSRobots.UNKNOWN

    @staticmethod
    def create_description_for(name: str) -> RobotDescription:
        """
        Create a robot model description for the given name.
        """

        robot_id = RCSSRobots.from_value(name)

        if robot_id == RCSSRobots.NAO1:
            return RCSSNao1Description()
        if robot_id == RCSSRobots.NAO2:
            return RCSSNao2Description()
        if robot_id == RCSSRobots.NAO3:
            return RCSSNao3Description()
        if robot_id in (RCSSRobots.NAO4, RCSSRobots.NAO_TOE):
            return RCSSNao4Description()

        # cases: NAO, NAO0 and UNKNOWN
        return RCSSNaoHeteroDescription()


class RCSSSensorType(Enum):
    """
    Specific sensor types used in RoboCup Soccer Simulation.
    """

    FORCE_RESISTANCE = 'force_resistance'
    """
    A force sensor, receiving force information.
    """


class RCSSActuatorType(Enum):
    """
    Specific actuator types used in RoboCup Soccer Simulation.
    """

    SCENE = 'scene'
    """
    A scene actuator for spawning a robot.
    """

    INIT = 'init'
    """
    A init actuator for initializing a robot.
    """

    SYNC = 'sync'
    """
    A synchronize actuator.
    """

    BEAM = 'beam'
    """
    A beam actuator.
    """

    PASS_MODE = 'pass_mode'  # noqa: S105 - prevent ruff hardcoded-passwort-assignment warning
    """
    A pass mode actuator.
    """


@dataclass(frozen=True)
class ForceResistanceDescription(SensorDescription):
    """
    Default force resistance sensor description.
    """

    def __init__(self, name: str, frame_id: str, perceptor_name: str):
        super().__init__(name, frame_id, perceptor_name, RCSSSensorType.FORCE_RESISTANCE.value)


@dataclass(frozen=True)
class SceneDescription(ActuatorDescription):
    """
    Default scene actuator description.
    """

    scene: str
    """
    The scene path.
    """

    model_type: int
    """
    The model type id.
    """

    def __init__(self, name: str, effector_name: str, scene: str, model_type: int):
        super().__init__(name, effector_name, RCSSActuatorType.SCENE.value)

        object.__setattr__(self, 'scene', scene)
        object.__setattr__(self, 'model_type', model_type)


@dataclass(frozen=True)
class InitDescription(ActuatorDescription):
    """
    Default init actuator description.
    """

    def __init__(self, name: str, effector_name: str):
        super().__init__(name, effector_name, RCSSActuatorType.INIT.value)


@dataclass(frozen=True)
class SyncDescription(ActuatorDescription):
    """
    Default synchronize actuator description.
    """

    auto_sync: bool
    """
    Flag for enabling auto sync.
    """

    def __init__(self, name: str, effector_name: str, *, auto_sync: bool = True):
        super().__init__(name, effector_name, RCSSActuatorType.SYNC.value)

        object.__setattr__(self, 'auto_sync', auto_sync)


@dataclass(frozen=True)
class BeamDescription(ActuatorDescription):
    """
    Default beam actuator description.
    """

    def __init__(self, name: str, effector_name: str):
        super().__init__(name, effector_name, RCSSActuatorType.BEAM.value)


@dataclass(frozen=True)
class PassModeDescription(ActuatorDescription):
    """
    Default pass mode actuator description.
    """

    def __init__(self, name: str, effector_name: str):
        super().__init__(name, effector_name, RCSSActuatorType.PASS_MODE.value)


class RCSSNaoHeteroDescription(RobotDescription):
    """
    Base description for the Nao-Hetero model used in the RoboCup Soccer Simulation.
    """

    def __init__(self, model_subtype: int = 0) -> None:
        """
        Construct a new Nao-Hetero model.
        """

        super().__init__(f'{RCSSRobots.NAO.value}{model_subtype}')

        s45 = sin(pi / 4.0)

        # fmt: off
        # bodies                              name,                    (                origin),  mass),                   (                origin), (      dimensions)
        self._add_body(BodyDescription(    'torso', InertiaDescription((     0,      0,      0), 1.217), VisualDescription((     0,      0,      0), (0.10, 0.10, 0.18))))
        # head
        self._add_body(BodyDescription(     'neck', InertiaDescription((     0,      0,      0), 0.050), VisualDescription((     0,      0,      0), (0.03, 0.03, 0.08))))
        self._add_body(BodyDescription(     'head', InertiaDescription((     0,      0,  0.005), 0.350), VisualDescription((     0,      0,  0.005), (0.13, 0.13, 0.13))))
        self._add_body(BodyDescription(   'camera'))
        # right arm
        self._add_body(BodyDescription('rshoulder', InertiaDescription((     0,      0,      0), 0.070), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('rupperarm', InertiaDescription(( 0.020, -0.010,      0), 0.150), VisualDescription(( 0.020, -0.010,      0), (0.08, 0.07, 0.06))))
        self._add_body(BodyDescription(   'relbow', InertiaDescription((     0,      0,      0), 0.035), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('rlowerarm', InertiaDescription(( 0.050,      0,      0), 0.200), VisualDescription(( 0.050,      0,      0), (0.11, 0.05, 0.05))))
        # right leg
        self._add_body(BodyDescription(    'rhip1', InertiaDescription((     0,      0,      0), 0.090), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'rhip2', InertiaDescription((     0,      0,      0), 0.125), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(  'rthight', InertiaDescription(( 0.010,      0, -0.040), 0.275), VisualDescription(( 0.010,      0, -0.040), (0.07, 0.07, 0.14))))
        self._add_body(BodyDescription(   'rshank', InertiaDescription(( 0.010,      0, -0.045), 0.225), VisualDescription(( 0.010,      0, -0.045), (0.07, 0.08, 0.11))))
        self._add_body(BodyDescription(   'rankle', InertiaDescription((     0,      0,      0), 0.125), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'rfoot', InertiaDescription(( 0.030,      0, -0.040), 0.200), VisualDescription(( 0.030,      0, -0.040), (0.16, 0.08, 0.02))))
        # left arm
        self._add_body(BodyDescription('lshoulder', InertiaDescription((     0,      0,      0), 0.070), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('lupperarm', InertiaDescription(( 0.020,  0.010,      0), 0.150), VisualDescription(( 0.020,  0.010,      0), (0.08, 0.07, 0.06))))
        self._add_body(BodyDescription(   'lelbow', InertiaDescription((     0,      0,      0), 0.035), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('llowerarm', InertiaDescription(( 0.050,      0,      0), 0.200), VisualDescription(( 0.050,      0,      0), (0.11, 0.05, 0.05))))
        # left leg
        self._add_body(BodyDescription(    'lhip1', InertiaDescription((     0,      0,      0), 0.090), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'lhip2', InertiaDescription((     0,      0,      0), 0.125), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(  'lthight', InertiaDescription(( 0.010,      0, -0.040), 0.275), VisualDescription(( 0.010,      0, -0.040), (0.07, 0.07, 0.14))))
        self._add_body(BodyDescription(   'lshank', InertiaDescription(( 0.010,      0, -0.045), 0.225), VisualDescription(( 0.010,      0, -0.045), (0.07, 0.08, 0.11))))
        self._add_body(BodyDescription(   'lankle', InertiaDescription((     0,      0,      0), 0.125), VisualDescription((     0,      0,      0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'lfoot', InertiaDescription(( 0.030,      0, -0.040), 0.200), VisualDescription(( 0.030,      0, -0.040), (0.16, 0.08, 0.02))))

        # joints                                          name, parent body,   child body, perceptor, (                anchor),           axis, (   limits),            motor(effetor, max_speed, max_torque)
        # head
        self._add_joint(HingeJointDescription(       'NeckYaw',     'torso',       'neck',     'hj1', (     0,      0,  0.090),     V3D_UNIT_Z, (-120, 120), MotorDescription(  'he1',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(     'NeckPitch',      'neck',       'head',     'hj2', (     0,      0,  0.060), V3D_UNIT_NEG_Y, ( -45,  45), MotorDescription(  'he2',      7.03,        0.0)))
        self._add_joint(FixedJointDescription(   'CameraJoint',      'head',     'camera',            (     0,      0,  0.005)))
        # right arm
        self._add_joint(HingeJointDescription('RShoulderPitch',     'torso',  'rshoulder',    'raj1', (     0, -0.098,  0.075), V3D_UNIT_NEG_Y, (-120, 120), MotorDescription( 'rae1',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(  'RShoulderYaw', 'rshoulder',  'rupperarm',    'raj2', (     0,      0,      0),     V3D_UNIT_Z, ( -95,   1), MotorDescription( 'rae2',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(      'RArmRoll', 'rupperarm',     'relbow',    'raj3', ( 0.090,      0,  0.009),     V3D_UNIT_X, (-120, 120), MotorDescription( 'rae3',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(       'RArmYaw',    'relbow',  'rlowerarm',    'raj4', (     0,      0,      0),     V3D_UNIT_Z, (  -1,  90), MotorDescription( 'rae4',      7.03,        0.0)))
        # right leg
        self._add_joint(HingeJointDescription(  'RHipYawPitch',     'torso',      'rhip1',    'rlj1', (-0.010, -0.055, -0.115),  (0, s45, s45), ( -90,   1), MotorDescription( 'rle1',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(      'RHipRoll',     'rhip1',      'rhip2',    'rlj2', (     0,      0,      0),     V3D_UNIT_X, ( -45,  25), MotorDescription( 'rle2',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(     'RHipPitch',     'rhip2',    'rthight',    'rlj3', (     0,      0,      0), V3D_UNIT_NEG_Y, ( -25, 100), MotorDescription( 'rle3',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(    'RKneePitch',   'rthight',     'rshank',    'rlj4', ( 0.005,      0, -0.120), V3D_UNIT_NEG_Y, (-130,   1), MotorDescription( 'rle4',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(    'RFootPitch',    'rshank',     'rankle',    'rlj5', (     0,      0, -0.100), V3D_UNIT_NEG_Y, ( -45,  75), MotorDescription( 'rle5',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(     'RFootRoll',    'rankle',      'rfoot',    'rlj6', (     0,      0,      0),     V3D_UNIT_X, ( -25,  45), MotorDescription( 'rle6',      7.03,        0.0)))
        # left arm
        self._add_joint(HingeJointDescription('LShoulderPitch',     'lorso',  'lshoulder',    'laj1', (     0,  0.098,  0.075), V3D_UNIT_NEG_Y, (-120, 120), MotorDescription( 'lae1',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(  'LShoulderYaw', 'lshoulder',  'lupperarm',    'laj2', (     0,      0,      0),     V3D_UNIT_Z, (  -1,  95), MotorDescription( 'lae2',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(      'LArmRoll', 'lupperarm',     'lelbow',    'laj3', ( 0.090,      0,  0.009),     V3D_UNIT_X, (-120, 120), MotorDescription( 'lae3',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(       'LArmYaw',    'lelbow',  'llowerarm',    'laj4', (     0,      0,      0),     V3D_UNIT_Z, ( -90,   1), MotorDescription( 'lae4',      7.03,        0.0)))
        # left leg
        self._add_joint(HingeJointDescription(  'LHipYawPitch',     'lorso',      'lhip1',    'llj1', (-0.010,  0.055, -0.115), (0, s45, -s45), ( -90,   1), MotorDescription( 'lle1',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(      'LHipRoll',     'lhip1',      'lhip2',    'llj2', (     0,      0,      0),     V3D_UNIT_X, ( -25,  45), MotorDescription( 'lle2',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(     'LHipPitch',     'lhip2',    'lthight',    'llj3', (     0,      0,      0), V3D_UNIT_NEG_Y, ( -25, 100), MotorDescription( 'lle3',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(    'LKneePitch',   'lthight',     'lshank',    'llj4', ( 0.005,      0, -0.120), V3D_UNIT_NEG_Y, (-130,   1), MotorDescription( 'lle4',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(    'LFootPitch',    'lshank',     'lankle',    'llj5', (     0,      0, -0.100), V3D_UNIT_NEG_Y, ( -45,  75), MotorDescription( 'lle5',      7.03,        0.0)))
        self._add_joint(HingeJointDescription(     'LFootRoll',    'lankle',      'lfoot',    'llj6', (     0,      0,      0),     V3D_UNIT_X, ( -45,  25), MotorDescription( 'lle6',      7.03,        0.0)))
        # fmt: off

        # virtual actuators
        self._add_actuator(SceneDescription('create', 'scene', 'rsg/agent/nao/nao_hetero.rsg', model_subtype))
        self._add_actuator(InitDescription('init', 'init'))
        self._add_actuator(SyncDescription('sync', 'syn', auto_sync=True))
        self._add_actuator(BeamDescription('beam', 'beam'))
        self._add_actuator(PassModeDescription('pass_mode', 'pass'))

        # sensors
        # gyro rate
        self._add_sensor(GyroDescription('torso_gyro', 'torso', 'torso_gyro'))

        # accelerometer
        self._add_sensor(AccelerometerDescription('torso_acc', 'torso', 'torso_acc'))

        # camera
        self._add_sensor(CameraDescription('camera', 'camera', 'See', 120, 120))

        # force
        self._add_sensor(ForceResistanceDescription('RFootForce', 'rfoot', 'rf'))
        self._add_sensor(ForceResistanceDescription('LFootForce', 'lfoot', 'lf'))


class RCSSNao1Description(RCSSNaoHeteroDescription):
    """
    Base description for the Nao-Hetero type 1 model used in the RoboCup Soccer Simulation.
    """

    def __init__(self) -> None:
        """
        Construct a new Nao-Hetero model.
        """

        super().__init__(1)

        # fmt: off
        # # bodies                          name,                    (             origin),  mass),                   (             origin), (      dimensions)
        self._add_body(BodyDescription('rthight', InertiaDescription(( 0.010, 0, -0.05832), 0.275), VisualDescription(( 0.010, 0, -0.05832), (0.07, 0.07, 0.14))), override=True)
        self._add_body(BodyDescription('lthight', InertiaDescription(( 0.010, 0, -0.05832), 0.275), VisualDescription(( 0.010, 0, -0.05832), (0.07, 0.07, 0.14))), override=True)

        # joints                                      name, parent body, child body, perceptor, (              anchor),           axis, (   limits),            motor(effetor, max_speed, max_torque)
        self._add_joint(HingeJointDescription(  'RArmRoll', 'rupperarm',   'relbow',    'raj3', (0.12664, 0,  0.00900),     V3D_UNIT_X, (-120, 120), MotorDescription( 'rae3',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription('RKneePitch',   'rthight',   'rshank',    'rlj4', (0.00500, 0, -0.13832), V3D_UNIT_NEG_Y, (-130,   1), MotorDescription( 'rle4',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription('RFootPitch',    'rshank',   'rankle',    'rlj5', (      0, 0, -0.11832), V3D_UNIT_NEG_Y, ( -45,  75), MotorDescription( 'rle5',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription(  'LArmRoll', 'lupperarm',   'lelbow',    'laj3', (0.12664, 0,  0.00900),     V3D_UNIT_X, (-120, 120), MotorDescription( 'lae3',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription('LKneePitch',   'lthight',   'lshank',    'llj4', (0.00500, 0, -0.13832), V3D_UNIT_NEG_Y, (-130,   1), MotorDescription( 'lle4',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription('LFootPitch',    'lshank',   'lankle',    'llj5', (      0, 0, -0.11832), V3D_UNIT_NEG_Y, ( -45,  75), MotorDescription( 'lle5',      7.03,        0.0)), override=True)
        # fmt: on


class RCSSNao2Description(RCSSNaoHeteroDescription):
    """
    Base description for the Nao-Hetero type 2 model used in the RoboCup Soccer Simulation.
    """

    def __init__(self) -> None:
        """
        Construct a new Nao-Hetero type 2 model.
        """

        super().__init__(2)

        # fmt: off
        # joints                                      name, parent body, child body, perceptor, (      anchor),           axis, (  limits),            motor(effetor, max_speed, max_torque)
        self._add_joint(HingeJointDescription('RFootPitch',    'rshank',   'rankle',    'rlj5', (0, 0, -0.100), V3D_UNIT_NEG_Y, (-45,  75), MotorDescription( 'rle5',   8.80667,        0.0)), override=True)
        self._add_joint(HingeJointDescription( 'RFootRoll',    'rankle',    'rfoot',    'rlj6', (0, 0,      0),     V3D_UNIT_X, (-25,  45), MotorDescription( 'rle6',   3.47234,        0.0)), override=True)

        self._add_joint(HingeJointDescription('LFootPitch',    'lshank',   'lankle',    'llj5', (0, 0, -0.100), V3D_UNIT_NEG_Y, (-45,  75), MotorDescription( 'lle5',   8.80667,        0.0)), override=True)
        self._add_joint(HingeJointDescription( 'LFootRoll',    'lankle',    'lfoot',    'llj6', (0, 0,      0),     V3D_UNIT_X, (-45,  25), MotorDescription( 'lle6',   3.47234,        0.0)), override=True)
        # fmt: on


class RCSSNao3Description(RCSSNaoHeteroDescription):
    """
    Base description for the Nao-Hetero type 3 model used in the RoboCup Soccer Simulation.
    """

    def __init__(self) -> None:
        """
        Construct a new Nao-Hetero type 3 model.
        """

        super().__init__(3)

        s45 = sin(pi / 4)

        # fmt: off
        # # bodies                          name,                    (             origin),  mass),                   (             origin), (      dimensions)
        self._add_body(BodyDescription('rthight', InertiaDescription(( 0.010, 0, -0.06787), 0.275), VisualDescription(( 0.010, 0, -0.06787), (0.07, 0.07, 0.14))), override=True)
        self._add_body(BodyDescription('lthight', InertiaDescription(( 0.010, 0, -0.06787), 0.275), VisualDescription(( 0.010, 0, -0.06787), (0.07, 0.07, 0.14))), override=True)

        # joints                                        name, parent body, child body, perceptor, (                      anchor),           axis, (   limits),            motor(effetor, max_speed, max_torque)
        self._add_joint(HingeJointDescription(    'RArmRoll', 'rupperarm',   'relbow',    'raj3', ( 0.14573,        0,  0.00900),     V3D_UNIT_X, (-120, 120), MotorDescription( 'rae3',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription('RHipYawPitch',     'torso',    'rhip1',    'rlj1', (-0.01000, -0.07295, -0.11500),  (0, s45, s45), ( -90,   1), MotorDescription( 'rle1',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription(  'RKneePitch',   'rthight',   'rshank',    'rlj4', ( 0.00500,        0, -0.14787), V3D_UNIT_NEG_Y, (-130,   1), MotorDescription( 'rle4',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription(  'RFootPitch',    'rshank',   'rankle',    'rlj5', (       0,        0, -0.12787), V3D_UNIT_NEG_Y, ( -45,  75), MotorDescription( 'rle5',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription(    'LArmRoll', 'lupperarm',   'lelbow',    'laj3', ( 0.14573,        0,  0.00900),     V3D_UNIT_X, (-120, 120), MotorDescription( 'lae3',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription('LHipYawPitch',     'lorso',    'lhip1',    'llj1', (-0.01000,  0.07295, -0.11500), (0, s45, -s45), ( -90,   1), MotorDescription( 'lle1',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription(  'LKneePitch',   'lthight',   'lshank',    'llj4', ( 0.00500,        0, -0.14787), V3D_UNIT_NEG_Y, (-130,   1), MotorDescription( 'lle4',      7.03,        0.0)), override=True)
        self._add_joint(HingeJointDescription(  'LFootPitch',    'lshank',   'lankle',    'llj5', (       0,        0, -0.12787), V3D_UNIT_NEG_Y, ( -45,  75), MotorDescription( 'lle5',      7.03,        0.0)), override=True)
        # fmt: on


class RCSSNao4Description(RCSSNaoHeteroDescription):
    """
    Base description for the Nao-Hetero type 4 (toe) model used in the RoboCup Soccer Simulation.
    """

    def __init__(self) -> None:
        """
        Construct a new Nao-Hetero type 4 (toe) model.
        """

        super().__init__(4)

        # fmt: off
        # bodies                          name, position(     x,      y,      z)
        self._add_body(BodyDescription('rfoot', InertiaDescription((0.01224, 0, -0.040), 0.1556), VisualDescription((0.01224, 0, -0.040), (0.12448, 0.08, 0.02))), override=True)
        self._add_body(BodyDescription( 'rtoe', InertiaDescription((0.01776, 0,  0.005), 0.0444), VisualDescription((0.01776, 0,  0.005), (0.03552, 0.08, 0.01))))
        self._add_body(BodyDescription('lfoot', InertiaDescription((0.01224, 0, -0.040), 0.1556), VisualDescription((0.01224, 0, -0.040), (0.12448, 0.08, 0.02))), override=True)
        self._add_body(BodyDescription( 'ltoe', InertiaDescription((0.01776, 0,  0.005), 0.0444), VisualDescription((0.01776, 0,  0.005), (0.03552, 0.08, 0.01))))

        # joints                                     name, parent body, child body, perceptor, (            anchor),       axis, (  limits),            motor(effetor, max_speed, max_torque)
        self._add_joint(HingeJointDescription('RToePitch',     'rfoot',     'rtoe',    'rlj7', (0.07448, 0, -0.050), V3D_UNIT_Y, ( -1,  70), MotorDescription( 'rle7',      7.03,        0.0)))
        self._add_joint(HingeJointDescription('LToePitch',     'lfoot',     'ltoe',    'llj7', (0.07448, 0, -0.050), V3D_UNIT_Y, ( -1,  70), MotorDescription( 'lle7',      7.03,        0.0)))

        # force sensors
        self._add_sensor(ForceResistanceDescription('RToeForce', 'rtoe', 'rf1'))
        self._add_sensor(ForceResistanceDescription('LToeForce', 'ltoe', 'lf1'))
        # fmt: on
