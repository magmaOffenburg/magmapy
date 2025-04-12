from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from magma.agent.communication.perception import Perception


class PByteMessageParser(Protocol):
    """
    Protocol for byte based message parsers.
    """

    def parse(self, msg: bytes | bytearray) -> Perception:
        """
        Parse the given message into a list of perceptors.
        """


class PTextMessageParser(Protocol):
    """
    Protocol for text based message parsers.
    """

    def parse(self, msg: str) -> Perception:
        """
        Parse the given message into a list of perceptors.
        """


class ByteTextMessageParser:
    """
    Wrapper class wrapping a text message parser into a byte message parser.
    """

    def __init__(self, parser: PTextMessageParser) -> None:
        """
        Construct a new byte text message parser wrapper.
        """

        self._parser: PTextMessageParser = parser


    def parse(self, msg: bytes | bytearray) -> Perception:
        """
        Parse the given message into a list of perceptors.
        """

        return self._parser.parse(msg.decode())
