from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from queue import Queue

    from magma.agent.communication.action import Action
    from magma.agent.communication.channel import PCommunicationChannel
    from magma.agent.communication.perception import Perception


class PChannelManager(Protocol):
    """The channel manager protocol definition."""

    def start(self, perception_queue: Queue[Perception]) -> bool:
        """Start all registered channels.

        Parameter
        ---------
        perception_queue : Queue[Perception]
            The queue to which incoming perceptions are handed for processing.
        """

    def stop(self) -> None:
        """Stop all active channels again."""

    def is_running(self) -> bool:
        """Flag, if the channel manager is currently running or not."""

    def send_action(self, action: Action) -> None:
        """Send the action commands of the given action map.

        Parameter
        ---------
        action : Action
            The collection of actions to send.
        """


class DefaultChannelManager:
    """Default channel manager implementation."""

    def __init__(self) -> None:
        """Construct a new channel manager."""

        self._channels: list[PCommunicationChannel] = []
        """The list of registered channels."""

        self._perception_queue: Queue[Perception] | None = None
        """The queue to which incoming perceptions are forwarded."""

    def register_channel(self, channel: PCommunicationChannel) -> None:
        """Register a channel to the manager.

        Parameter
        ---------
        channel : PCommunicationChannel
            The new communication channel to register.
        """

        self._channels.append(channel)

        # automatically start channel in case the channel manager is running
        if self._perception_queue is not None:
            channel.start(self._perception_queue)

    def start(self, perception_queue: Queue[Perception]) -> bool:
        """Start all registered channels.

        Parameter
        ---------
        perception_queue : Queue[Perception]
            The queue to which incoming perceptions are handed for processing.
        """

        self._perception_queue = perception_queue

        # start individual channels
        for channel in self._channels:
            try:
                channel.start(self._perception_queue)
            except ConnectionError:
                print(f'ERROR: "{channel.get_name()}" connection could not be established!')  # noqa: T201
                self.stop()
                return False

        return True

    def stop(self) -> None:
        """Stop all active channels again."""

        for channel in self._channels:
            channel.stop()

        self._perception_queue = None

    def is_running(self) -> bool:
        """Flag, if the channel manager is active or not."""

        return self._perception_queue is not None

    def send_action(self, action: Action) -> None:
        """Send the action commands of the given action map.

        Parameter
        ---------
        action : Action
            The collection of actions to send.
        """

        # forward actions to individual channels
        for channel in self._channels:
            channel.send_action(action)
