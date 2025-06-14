from __future__ import annotations

import argparse
import signal
from typing import TYPE_CHECKING

from magma.agent.runtime.agent_runtime import AgentRuntime
from magma.rcss.model.robot.rcsssmj_robot_description import RCSSSMJRobots
from magma.rcss.model.robot.spark_robot_description import SimSparkRobots
from magma.rcss.model.world.rcss_field_description import RCSSFieldVersion
from magma.rcss.runtime.rcsssmj_factory import RCSSSMJAgentFactory
from magma.rcss.runtime.spark_factory import SimSparkAgentFactory

if TYPE_CHECKING:
    from types import FrameType


def magma_agent() -> None:
    """Main function for running a magma agent."""

    # there currently only exists a RCSS agent main, so simply forward to that one
    rcsssmj_agent()


def rcss_agent() -> None:
    """Main function for running a magma RCSS agent."""

    # fetch argument options
    field_versions: list[str] = [str(version.value) for version in RCSSFieldVersion if version != RCSSFieldVersion.UNKNOWN]
    robot_models: list[str] = ['default'] + [str(robot.value) for robot in SimSparkRobots if robot != SimSparkRobots.UNKNOWN]
    decision_maker_ids: list[str] = ['default', 'Soccer']

    # parse arguments
    parser = argparse.ArgumentParser(description='The magma agent framework.')

    # fmt: off
    parser.add_argument('-t', '--teamname',      type=str, help='The team name.',             default='magma',            required=False)
    parser.add_argument('-n', '--playerno',      type=int, help='The player number.',         default=1,                  required=False)
    parser.add_argument('-r', '--robot',         type=str, help='The robot model.',           default='default',          required=False, choices=robot_models)
    parser.add_argument('-s', '--server',        type=str, help='The server address.',        default='127.0.0.1',        required=False)
    parser.add_argument('-p', '--port',          type=int, help='The server port.',           default=3100,               required=False)
    parser.add_argument('-f', '--field',         type=str, help='The field version.',         default=field_versions[-1], required=False, choices=field_versions)
    parser.add_argument('-d', '--decisionmaker', type=str, help='The decision maker to use.', default='default',          required=False, choices=decision_maker_ids)
    # fmt: on

    args = parser.parse_args()

    # create agent runtime
    factory = SimSparkAgentFactory(args.teamname, args.playerno, args.robot, args.server, args.port, args.field, args.decisionmaker)
    agent: AgentRuntime = AgentRuntime(factory)

    # register SIGINT handler
    def signal_handler(sig: int, frame: FrameType | int | signal.Handlers | None) -> None:
        del sig, frame  # signal unused parameter
        agent.shutdown()

    signal.signal(signal.SIGINT, signal_handler)

    # run agent
    agent.run()


def rcsssmj_agent() -> None:
    """Main function for running a magma RCSSSMJ agent."""

    # fetch argument options
    field_versions: list[str] = [str(version.value) for version in RCSSFieldVersion if version != RCSSFieldVersion.UNKNOWN]
    robot_models: list[str] = ['default'] + [str(robot.value) for robot in RCSSSMJRobots if robot != RCSSSMJRobots.UNKNOWN]
    decision_maker_ids: list[str] = ['default', 'Soccer']

    # parse arguments
    parser = argparse.ArgumentParser(description='The magma agent framework.')

    # fmt: off
    parser.add_argument('-t', '--teamname',      type=str, help='The team name.',             default='magma',            required=False)
    parser.add_argument('-n', '--playerno',      type=int, help='The player number.',         default=1,                  required=False)
    parser.add_argument('-r', '--robot',         type=str, help='The robot model.',           default='default',          required=False, choices=robot_models)
    parser.add_argument('-s', '--server',        type=str, help='The server address.',        default='127.0.0.1',        required=False)
    parser.add_argument('-p', '--port',          type=int, help='The server port.',           default=60000,              required=False)
    parser.add_argument('-f', '--field',         type=str, help='The field version.',         default=field_versions[-1], required=False, choices=field_versions)
    parser.add_argument('-d', '--decisionmaker', type=str, help='The decision maker to use.', default='default',          required=False, choices=decision_maker_ids)
    # fmt: on

    args = parser.parse_args()

    # create agent runtime
    factory = RCSSSMJAgentFactory(args.teamname, args.playerno, args.robot, args.server, args.port, args.field, args.decisionmaker)
    agent: AgentRuntime = AgentRuntime(factory)

    # register SIGINT handler
    def signal_handler(sig: int, frame: FrameType | int | signal.Handlers | None) -> None:
        del sig, frame  # signal unused parameter
        agent.shutdown()

    signal.signal(signal.SIGINT, signal_handler)

    # run agent
    agent.run()


if __name__ == '__main__':
    magma_agent()
