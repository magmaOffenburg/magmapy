from abc import ABC, abstractmethod
from queue import Queue
from typing import Protocol

from magma.agent.communication.action import Action
from magma.agent.communication.perception import Perception


class PCommunicationChannel(Protocol):
    """
    Protocol for communication channels.
    """

    def get_name(self) -> str:
        """
        Retrieve the unique name of the channel.
        """

    def start(self, perceptions_queue: Queue[Perception]) -> None:
        """
        Start the channel.
        """

    def stop(self) -> bool:
        """
        Stop the channel.
        """

    def is_running(self) -> bool:
        """
        Flag if this channel is active or not.
        """

    def send_action(self, action: Action) -> None:
        """
        Send the action commands of the given action map.
        """


class CommunicationChannelBase(ABC):
    """
    Base class for communication channel implementations.
    """

    def __init__(self, name: str) -> None:
        """
        Construct a new communication channel.
        """

        super().__init__()

        self._name: str = name

    def get_name(self) -> str:
        """
        Retrieve the unique name of the channel.
        """

        return self._name

    @abstractmethod
    def start(self, perceptions_queue: Queue[Perception]) -> None:
        """
        Start the channel.
        """

    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the channel.
        """

    @abstractmethod
    def is_running(self) -> bool:
        """
        Flag if this channel is active or not.
        """

    @abstractmethod
    def send_action(self, action: Action) -> None:
        """
        Send the action commands of the given action map.
        """
