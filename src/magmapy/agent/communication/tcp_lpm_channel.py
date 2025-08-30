from __future__ import annotations

import socket
from threading import Thread
from typing import TYPE_CHECKING

from magmapy.agent.communication.channel import CommunicationChannelBase
from magmapy.agent.communication.perception import Perception

if TYPE_CHECKING:
    from queue import Queue

    from magmapy.agent.communication.action import Action
    from magmapy.agent.communication.msg_encoder import PByteMessageEncoder
    from magmapy.agent.communication.msg_parser import PByteMessageParser


class TCPLPMChannel(CommunicationChannelBase):
    """TCP/IP channel implementation for receiving and sending (4-byte) length prefixed messages."""

    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        parser: PByteMessageParser,
        encoder: PByteMessageEncoder,
        length_prefix_size: int = 4,
    ) -> None:
        """Construct a new TCP/IP channel.

        Parameter
        ---------
        name : str
            The name of the channel.

        host : str
            The server IP or hostname.

        port : int
            The server port.

        parser : PByteMessageParser
            The message parser instance for parsing incoming messages.

        encoder : PByteMessageEncoder
            The message encoder for encoding outgoing messages.

        length_prefix_size : int, default=4
            The message size prefix length in bytes.
        """

        super().__init__(name)

        self._host: str = host
        """The server IP or hostname."""

        self._port: int = port
        """The server port."""

        self._parser: PByteMessageParser = parser
        """The parser instance for parsing incoming perception messages."""

        self._encoder: PByteMessageEncoder = encoder
        """The encoder instance for encoding outgoing action messages."""

        self._length_prefix_size: int = length_prefix_size
        """The message size prefix length in bytes."""

        self._socket: socket.socket | None = None
        """The TCP/IP socket."""

        self._rcv_buffer_size = 8192
        """The current size of the receive buffer."""

        self._rcv_buffer = bytearray(self._rcv_buffer_size)
        """A buffer for receiving messages."""

        self._receive_thread: Thread | None = None
        """The thread running the receive loop."""

        self._shutdown: bool = False
        """Flag indicating if the channel should shutdown."""

        self._perceptions_queue: Queue[Perception] | None = None
        """The queue to which to forward incoming perceptions."""

    def start(self, perceptions_queue: Queue[Perception]) -> None:
        if self._socket is None:
            self._shutdown = False
            self._perceptions_queue = perceptions_queue

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # set TCP_NODELAY option to send messages immediately (without buffering)
            self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            try:
                self._socket.connect((self._host, self._port))
            except ConnectionError:
                self._socket.close()
                self._socket = None
                raise

            self._receive_thread = Thread(target=self.receive_loop, name=self._name)
            self._receive_thread.setDaemon(True)
            self._receive_thread.start()

    def stop(self) -> bool:
        # notify receive thread to shutdown
        self._shutdown = True

        # wait for the receiving thread to finish
        if self._receive_thread is not None:
            self._receive_thread.join()

        return True

    def is_running(self) -> bool:
        return self._socket is not None

    def send_action(self, action: Action) -> None:
        self.send_message(self._encoder.encode(action))

    def send_message(self, msg: bytes | bytearray) -> None:
        """Send the given message.

        Parameter
        ---------
        msg : bytes | bytearray
            The message to send.
        """

        if self._socket is None:
            return

        self._socket.send((len(msg)).to_bytes(self._length_prefix_size, byteorder='big') + msg)

    def receive_loop(self) -> None:
        """Receive messages from the TCP/IP socket in a loop until the channel is shutdown."""

        if self._socket is None or self._perceptions_queue is None:
            return

        # print(f'{self._name}: Start receive loop!')

        while not self._shutdown:
            try:
                msg = self.receive_next_message()
            except ConnectionError:
                self._perceptions_queue.put(Perception(shutdown=True))
                break

            perception: Perception = self._parser.parse(msg)

            self._perceptions_queue.put(perception)

        # print(f'{self._name}: End receive loop')

        # close and clear socket on shutdown
        self._socket.close()
        self._socket = None

        self._perceptions_queue = None

    def receive_next_message(self) -> bytes:
        """Receive the next message from the TCP/IP socket."""

        if self._socket is None:
            raise ConnectionResetError

        # receive message length information
        if self._socket.recv_into(self._rcv_buffer, nbytes=self._length_prefix_size, flags=socket.MSG_WAITALL) != self._length_prefix_size:
            raise ConnectionResetError

        msg_size = int.from_bytes(self._rcv_buffer[: self._length_prefix_size], byteorder='big', signed=False)

        # ensure receive buffer is large enough to hold the message
        if msg_size > self._rcv_buffer_size:
            self._rcv_buffer_size = msg_size
            self._rcv_buffer = bytearray(self._rcv_buffer_size)

        # receive message with the specified length
        if self._socket.recv_into(self._rcv_buffer, nbytes=msg_size, flags=socket.MSG_WAITALL) != msg_size:
            raise ConnectionResetError

        return self._rcv_buffer[:msg_size]
