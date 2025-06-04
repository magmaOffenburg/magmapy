from __future__ import annotations

from enum import Enum

from magma.agent.model.robot.robot_description import (
    AccelerometerDescription,
    BodyDescription,
    CameraDescription,
    FixedJointDescription,
    GyroDescription,
    HingeJointDescription,
    InertiaDescription,
    MotorDescription,
    RobotDescription,
    VisualDescription,
)
from magma.common.math.geometry.vector import V3D_UNIT_X, V3D_UNIT_Y, V3D_UNIT_Z
from magma.rcss.model.robot.rcss_robot_description import BeamDescription, InitDescription, SyncDescription


class RCSSSMJRobots(Enum):
    """
    Enum specifying the available robot models within the RCSSSMJ simulator.
    """

    UNKNOWN = 'unknown'
    """
    Unknown robot model.
    """

    T1 = 'T1'
    """
    The T1 robot.
    """

    @staticmethod
    def from_value(name: str) -> RCSSSMJRobots:
        """
        Fetch the enum entry corresponding to the given name value.
        """

        for v in RCSSSMJRobots:
            if v.value == name:
                return v

        print(f'WARNING: Unknown RCSSMJ robot model: "{name}"!')  # noqa: T201

        return RCSSSMJRobots.UNKNOWN

    @staticmethod
    def create_description_for(name: str) -> RobotDescription:
        """
        Create a robot model description for the given name.
        """

        robot_id = RCSSSMJRobots.from_value(name)

        if robot_id == RCSSSMJRobots.T1:
            return T1Description()

        # cases: T1 and UNKNOWN
        return T1Description()


class T1Description(RobotDescription):
    """
    Description for the T1 model used in the RCSSMJ soccer simulation.
    """

    def __init__(self) -> None:
        """
        Construct a new T1 model.
        """

        super().__init__(RCSSSMJRobots.T1.value)

        # fmt: off
        # bodies                              name,                    ( origin), mass ,                   (       origin), (    dimensions)
        self._add_body(BodyDescription(    'torso', InertiaDescription((0, 0, 0), 11.7), VisualDescription((0.06, 0, 0.12), (0.15, 0.2, 0.3))))
        # head
        self._add_body(BodyDescription(     'neck', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(     'head', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0.01, 0, 0.11), (0.16, 0.16, 0.16))))
        self._add_body(BodyDescription(   'camera'))
        # left arm
        self._add_body(BodyDescription('lshoulder', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('lupperarm', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(   'lelbow', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('llowerarm', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        # right arm
        self._add_body(BodyDescription('rshoulder', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('rupperarm', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(   'relbow', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription('rlowerarm', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        # waist
        self._add_body(BodyDescription(     'waist', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        # left leg
        self._add_body(BodyDescription(    'lhip1', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'lhip2', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(  'lthight', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(   'lshank', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(   'lankle', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'lfoot', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        # right leg
        self._add_body(BodyDescription(    'rhip1', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'rhip2', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(  'rthight', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(   'rshank', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(   'rankle', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))
        self._add_body(BodyDescription(    'rfoot', InertiaDescription((0, 0, 0), 0.1), VisualDescription((0, 0, 0), (0.01, 0.01, 0.01))))

        # joints                                          name, parent body,   child body, perceptor, (                       anchor),       axis, (   limits),            motor(effetor, max_speed, max_torque)
        # head
        self._add_joint(HingeJointDescription(       'NeckYaw',     'torso',       'neck',     'q_hj1', ( 0.0625,   0,        0.243   ), V3D_UNIT_Z, ( -90,  90), MotorDescription(  'he1',      10.0,        7.0)))
        self._add_joint(HingeJointDescription(     'NeckPitch',      'neck',       'head',     'q_hj2', ( 0,        0,        0.06185 ), V3D_UNIT_Y, ( -20,  70), MotorDescription(  'he2',      10.0,        7.0)))
        self._add_joint(FixedJointDescription(   'CameraJoint',      'head',     'camera',              ( 0.05,     0,        0.12    )))
        # left arm
        self._add_joint(HingeJointDescription('LShoulderPitch',     'torso',  'lshoulder',    'q_laj1', ( 0.0575,   0.1063,   0.219   ), V3D_UNIT_Y, (-190,  70), MotorDescription( 'lae1',      10.0,       18.0)))
        self._add_joint(HingeJointDescription( 'LShoulderRoll', 'lshoulder',  'lupperarm',    'q_laj2', ( 0,        0.047,    0       ), V3D_UNIT_X, (-100,  90), MotorDescription( 'lae2',      10.0,       18.0)))
        self._add_joint(HingeJointDescription(     'LArmPitch', 'lupperarm',     'lelbow',    'q_laj3', ( 0.00025,  0.0605,   0       ), V3D_UNIT_Y, (-130, 130), MotorDescription( 'lae3',      10.0,       18.0)))
        self._add_joint(HingeJointDescription(       'LArmYaw',    'lelbow',  'llowerarm',    'q_laj4', ( 0,        0.1471,   0       ), V3D_UNIT_Z, (-140,   0), MotorDescription( 'lae4',      10.0,       18.0)))
        # right arm
        self._add_joint(HingeJointDescription('RShoulderPitch',     'torso',  'rshoulder',    'q_raj1', ( 0.0575,  -0.1063,   0.219   ), V3D_UNIT_Y, (-190,  70), MotorDescription( 'rae1',      10.0,       18.0)))
        self._add_joint(HingeJointDescription( 'RShoulderRoll', 'rshoulder',  'rupperarm',    'q_raj2', ( 0,       -0.047,    0       ), V3D_UNIT_X, ( -90, 100), MotorDescription( 'rae2',      10.0,       18.0)))
        self._add_joint(HingeJointDescription(     'RArmPitch', 'rupperarm',     'relbow',    'q_raj3', ( 0.00025, -0.0605,   0       ), V3D_UNIT_Y, (-130, 130), MotorDescription( 'rae3',      10.0,       18.0)))
        self._add_joint(HingeJointDescription(       'RArmYaw',    'relbow',  'rlowerarm',    'q_raj4', ( 0,       -0.1471,   0       ), V3D_UNIT_Z, (   0, 140), MotorDescription( 'rae4',      10.0,       18.0)))
        # waist
        self._add_joint(HingeJointDescription(      'WaistYaw',     'torso',      'waist',     'q_tj1', ( 0.0625,   0,       -0.1155  ), V3D_UNIT_Z, ( -90,  90), MotorDescription(  'te1',      10.0,       30.0)))
        # left leg
        self._add_joint(HingeJointDescription(     'LHipPitch',     'waist',      'lhip1',    'q_llj1', ( 0,        0.106,    0       ), V3D_UNIT_Y, (-103,  90), MotorDescription( 'lle1',      10.0,       45.0)))
        self._add_joint(HingeJointDescription(      'LHipRoll',     'lhip1',      'lhip2',    'q_llj2', ( 0,        0,       -0.02    ), V3D_UNIT_X, ( -11,  90), MotorDescription( 'lle2',      10.0,       30.0)))
        self._add_joint(HingeJointDescription(       'LHipYaw',     'lhip2',    'lthight',    'q_llj3', ( 0,        0,       -0.081854), V3D_UNIT_Z, ( -57,  57), MotorDescription( 'lle3',      10.0,       30.0)))
        self._add_joint(HingeJointDescription(    'LKneePitch',   'lthight',     'lshank',    'q_llj4', (-0.014,    0,       -0.134   ), V3D_UNIT_Y, (   0, 134), MotorDescription( 'lle4',      10.0,       60.0)))
        self._add_joint(HingeJointDescription(   'LAnklePitch',    'lshank',     'lankle',    'q_llj5', ( 0,        0,       -0.28    ), V3D_UNIT_Y, ( -50,  20), MotorDescription( 'lle5',      10.0,       20.0)))
        self._add_joint(HingeJointDescription(    'LAnkleRoll',    'lankle',      'lfoot',    'q_llj6', ( 0,        0.00025, -0.012   ), V3D_UNIT_X, ( -25,  25), MotorDescription( 'lle6',      10.0,       15.0)))
        # right leg
        self._add_joint(HingeJointDescription(     'RHipPitch',     'waist',      'rhip1',    'q_rlj1', ( 0,       -0.106,    0       ), V3D_UNIT_Y, (-103,  90), MotorDescription( 'rle1',      10.0,       45.0)))
        self._add_joint(HingeJointDescription(      'RHipRoll',     'rhip1',      'rhip2',    'q_rlj2', ( 0,        0,       -0.02    ), V3D_UNIT_X, ( -90,  11), MotorDescription( 'rle2',      10.0,       30.0)))
        self._add_joint(HingeJointDescription(       'RHipYaw',     'rhip2',    'rthight',    'q_rlj3', ( 0,        0,       -0.081854), V3D_UNIT_Z, ( -57,  57), MotorDescription( 'rle3',      10.0,       30.0)))
        self._add_joint(HingeJointDescription(    'RKneePitch',   'rthight',     'rshank',    'q_rlj4', (-0.014,    0,       -0.134   ), V3D_UNIT_Y, (   0, 134), MotorDescription( 'rle4',      10.0,       60.0)))
        self._add_joint(HingeJointDescription(   'RAnklePitch',    'rshank',     'rankle',    'q_rlj5', ( 0,        0,       -0.28    ), V3D_UNIT_Y, ( -50,  20), MotorDescription( 'rle5',      10.0,       20.0)))
        self._add_joint(HingeJointDescription(    'RAnkleRoll',    'rankle',      'rfoot',    'q_rlj6', ( 0,       -0.00025, -0.012   ), V3D_UNIT_X, ( -25,  25), MotorDescription( 'rle6',      10.0,       15.0)))
        # fmt: off

        # virtual actuators
        self._add_actuator(InitDescription('init', 'init', 'T1'))
        self._add_actuator(SyncDescription('sync', 'syn', auto_sync=True))
        self._add_actuator(BeamDescription('beam', 'beam'))

        # sensors
        # gyro rate
        self._add_sensor(GyroDescription('torso_gyro', 'torso', 'torso_gyro'))

        # accelerometer
        self._add_sensor(AccelerometerDescription('torso_acc', 'torso', 'torso_acc'))

        # camera
        self._add_sensor(CameraDescription('camera', 'camera', 'See', 120, 120))
