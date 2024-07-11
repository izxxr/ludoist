# MIT License

# Copyright (c) 2024 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple
from server import responses
from common.games import Game

import threading
import logging
import time
import json
import oblate

if TYPE_CHECKING:
    from server import LudoistServer
    import socket

__all__ = (
    "Connection",
)

_log = logging.getLogger(__name__)


class Connection(threading.Thread):
    """A client connection.

    Manages server's socket connection with a client in a separate thread.
    """

    def __init__(self, sock: socket.socket, addr: Tuple[str, int], server: LudoistServer) -> None:
        super().__init__(target=self._handler)

        self._sock = sock
        self._addr = addr
        self._server = server
        self._violations = 0
        self._last_violation_at = 0
        self._ping_interval = 40
        self._running = True
        self._keep_alive_thread = threading.Thread(target=self._keep_alive)
        self._ping_recv = threading.Event()
        self.start()

    def _inc_violation(self) -> None:
        self._violations += 1
        diff = time.time() - self._last_violation_at

        if diff > 300:
            self._violations = 0

        if diff < 300 and self._violations > 8:
            _log.info(f"Closing client {self._addr} - more than 8 violations within 5 minutes")
            self._close()

    def _send_data(self, data: Any = None) -> None:
        msg = json.dumps(data).encode()
        self._sock.send(msg)

    def _process_packet(self, packet: bytes):
        try:
            data = packet.decode()
            data = json.loads(data)
        except Exception:
            _log.error(f"{self._addr} sent unparsable data")
            msg = responses.make_error_message(responses.ERR_UNPARSABLE_DATA, "data could not be parsed as JSON")
            self._send_data(msg)
            self._inc_violation()
            return -1, None

        try:
            op_code = data["op"]
        except Exception:
            _log.error(f"{self._addr} sent data without OP code")
            msg = responses.make_error_message(responses.ERR_INVALID_DATA_FORMAT, "missing OP code")
            self._send_data(msg)
            self._inc_violation()
            return -1, None
        else:
            return op_code, data.get("d", None)

    def _listen(self) -> None:
        try:
            packet = self._sock.recv(3000)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            if self._running:
                _log.info(f"Client {self._addr} has closed the connection")
                self._close()

            return

        op, data = self._process_packet(packet)

        if op == -1:
            return

        if op == responses.OP_CODE_PING:
            return self._ping_recv.set()

        if op == responses.OP_CODE_REQUEST_GAMES:
            games = self._server.list_games()
            msg = responses.make_list_games_message(games)
            return self._send_data(msg)

        if op == responses.OP_CODE_CREATE_GAME:
            try:
                game = Game(data)  # type: ignore
            except oblate.ValidationError as e:
                msg = responses.make_error_message(
                    responses.ERR_GAME_CREATION_FAILED,
                    "invalid game data",
                    {"errors": e.raw()}
                )
                return self._send_data(msg)
            else:
                self._server.add_game(game)
                msg = responses.make_message(responses.OP_CODE_GAME_CREATED, game.dump())
                return self._send_data(msg)

        msg = responses.make_error_message(responses.ERR_INVALID_DATA_FORMAT, "invalid OP code")
        self._send_data(msg)
        self._inc_violation()

    def _keep_alive(self) -> None:
        while self._running:
            received = self._ping_recv.wait(timeout=self._ping_interval)

            if not received and self._running:
                _log.error(f"No PING received from {self._addr} - closing connection")
                msg = responses.make_error_message(responses.ERR_PING_TIMEOUT, "no PING received")
                self._send_data(msg)
                return self._close()

            if self._running:
                _log.debug(f"Received PING from {self._addr}")
                self._send_data(responses.make_pong_message())
                self._ping_recv.clear()

    def _setup(self) -> None:
        self._ping_recv.clear()
        self._keep_alive_thread = threading.Thread(target=self._keep_alive)
        self._keep_alive_thread.start()

    def _close(self) -> None:
        self._running = False
        self._sock.close()
        self._server._connections.pop(self._addr, None)

    def _handler(self) -> None:
        self._setup()
        # 10 seconds margin of error provided to account for any network delays
        self._send_data(responses.make_hello_message(self._ping_interval - 10))

        while self._running:
            self._listen()
