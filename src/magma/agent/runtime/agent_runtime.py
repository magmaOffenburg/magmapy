from queue import Empty, Queue
from typing import TYPE_CHECKING

from magma.agent.communication.perception import Perception
from magma.agent.runtime.factory import PAgentFactory

if TYPE_CHECKING:
    from magma.agent.communication.channel_manager import PChannelManager
    from magma.agent.decision.behavior import PBehavior
    from magma.agent.decision.decision_maker import PDecisionMaker
    from magma.agent.model.agent_model import PMutableAgentModel


class AgentRuntime:
    """The agent runtime is the top-level agent definition."""

    def __init__(self, factory: PAgentFactory) -> None:
        """Create a new agent.

        Parameter
        ---------
        factory : PAgentFactory
            The agent factory used to create the individual framework components.
        """

        # create agent components
        channel_manager, model, behaviors, decision = factory.create_agent_components()

        self._channel_manager: PChannelManager = channel_manager
        self._model: PMutableAgentModel = model
        self._behaviors: dict[str, PBehavior] = behaviors
        self._decision: PDecisionMaker = decision

        self._perception_queue: Queue[Perception] = Queue[Perception]()

    def run(self) -> None:
        """Run the agent."""

        # start channel manager
        if self._channel_manager.start(self._perception_queue):
            # perform an initial action (allowing the creation of simulation agents)
            self._act()

        # listen to incoming perceptions
        while self._channel_manager.is_running():
            try:
                perception = self._perception_queue.get(block=True, timeout=0.1)

                if perception.is_shutdown_requested():
                    # shutdown requested
                    self._channel_manager.stop()
                    break

                # update model
                self._model.update(perception)
                act = True

                if act:
                    # perform an action
                    self._act()

            except Empty:
                # no perception to process
                # print(f'No perception for 0.1 seconds!')
                pass

            except Exception as e:  # noqa: BLE001 - prevent blind exception catch warning
                print(e)  # noqa: T201

    def shutdown(self) -> None:
        """Shutdown agent runtime."""

        self._perception_queue.put(Perception(shutdown=True))

    def _act(self) -> None:
        """The central act method of the agent."""

        # decide and perform behaviors
        self._decision.decide()

        # generate actions from model
        action = self._model.generate_action()

        # send generated actions
        self._channel_manager.send_action(action)
