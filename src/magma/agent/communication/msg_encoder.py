from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from magma.agent.communication.action import Action


class PByteMessageEncoder(Protocol):
    """
    Protocol for byte based message encoders.
    """

    def encode(self, action: Action) -> bytes | bytearray:
        """
        Encode the given action commands into a message.
        """


class PTextMessageEncoder(Protocol):
    """
    Protocol for text based message encoders.
    """

    def encode(self, action: Action) -> str:
        """
        Encode the given action commands into a message.
        """


class ByteTextMessageEncoder:
    """
    Wrapper class wrapping a text message encoder into a byte message encoder.
    """

    def __init__(self, encoder: PTextMessageEncoder) -> None:
        """
        Construct a new byte text message encoder wrapper.
        """

        self._encoder: PTextMessageEncoder = encoder


    def encode(self, action: Action) -> bytes | bytearray:
        """
        Encode the given action commands into a message.
        """

        return self._encoder.encode(action).encode()
