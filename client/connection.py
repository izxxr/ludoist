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

from typing import TYPE_CHECKING, Tuple, Any, Optional, List, Dict
from server import responses
from common.games import Game

import socket
import threading
import logging
import time
import json
import concurrent.futures

if TYPE_CHECKING:
    from client.window import LudoistWindow

__all__ = (
    "Connection",
)

_log = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 4590


class Connection(threading.Thread):
    """Manages client's connection with the server."""

    def __init__(self, window: LudoistWindow) -> None:
        super().__init__(target=self._handler)

        self._window = window
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ping_interval = None
        self._keep_alive_thread = threading.Thread(target=self._keep_alive)
        self._pong_recv = threading.Event()
        self._futures: Dict[int, List[concurrent.futures.Future[Any]]] = {}
        self._running = False
        self._ready = threading.Event()
        self.latency = -1

    def _recv_packet(self) -> Tuple[int, Any]:
        try:
            packet = self._sock.recv(3000)
            data = json.loads(packet.decode())
        except Exception as e:
            if self._running:
                self._close()
                raise
            return -1, None
        else:
            return data["op"], data.get("d")

    def _listen(self) -> None:
        op, payload = self._recv_packet()

        if op == -1:
            return

        if op == responses.OP_CODE_HELLO:
            _log.info("HELLO received - handshake successful, starting keep-alive thread")

            self._ping_interval = payload["ping_interval"]
            self._keep_alive_thread.start()
            self._ready.set()

        if op == responses.OP_CODE_PONG:
            self._pong_recv.set()
            _log.info(f"PING acknowledged (latency {self.latency})")

        if op in self._futures:
            for fut in self._futures[op]:
                fut.set_result(payload)

    def _send_data(self, op_code: int, data: Any = None) -> None:
        msg = {"op": op_code}
        if data is not None:
            msg["d"] = data

        self._sock.send(json.dumps(msg).encode())

    def _keep_alive(self) -> None:
        assert self._ping_interval is not None

        while self._running:
            ping_at = time.time()
            self._send_data(responses.OP_CODE_PING)
            received = self._pong_recv.wait(timeout=20)

            if not received:
                _log.error("PONG not received from server - closing connection")
                self._close()
            else:
                self.latency = time.time() - ping_at

            time.sleep(self._ping_interval)
            self._pong_recv.clear()

    def _close(self) -> None:
        self._running = False
        self._sock.close()
        self._ready.clear()

    def _handler(self) -> None:
        self._running = True
        self._sock.connect((HOST, PORT))

        _log.info("Connected to server successfully - awaiting HELLO packet")

        while self._running:
            self._listen()

    def _wait_for(self, op_code: int, timeout: Optional[float] = None):
        fut = concurrent.futures.Future()
        try:
            futures = self._futures[op_code]
        except KeyError:
            self._futures[op_code] = [fut]
        else:
            futures.append(fut)

        result = fut.result(timeout=timeout)
        self._futures[op_code].remove(fut)

        return result

    def wait_until_ready(self) -> None:
        """Waits until connection has been established and handshake done"""
        self._ready.wait()

    def list_games(self) -> List[Game]:
        """Request the server to send the list of ongoing games."""
        self._send_data(responses.OP_CODE_REQUEST_GAMES)
        data = self._wait_for(responses.OP_CODE_LIST_GAMES)
        return [Game(g) for g in data]

    def create_game(self, name: str) -> Game:
        """Create a game."""
        self._send_data(responses.OP_CODE_CREATE_GAME, data={"name": name, "players": []})
        data = self._wait_for(responses.OP_CODE_GAME_CREATED)
        return Game(data)
