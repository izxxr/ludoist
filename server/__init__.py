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

from server.connection import Connection

import socket
import logging


__all__ = (
    "LudoistServer",
    "__version__",
)

__version__ = "1.0.0"

_log = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 4590


class LudoistServer:
    """The Ludoist server implementation.

    This class deals with the server's socket connection and stores/manages
    the state of ongoing games.
    """
    def __init__(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind((HOST, PORT))
        self._connections = {}
        self._running = False

    def start(self) -> None:
        """Starts the server and accepting clients."""
        try:
            self._runner()
        except KeyboardInterrupt:
            _log.info("Closing socket...")
            self._sock.detach()
            self._sock.close()

    def _runner(self) -> None:
        self._running = True
        self._sock.listen()

        _log.info("Server started - accepting clients")

        while self._running:
            client, addr = self._sock.accept()
            _log.info(f"Client {addr} connected")
            self._connections[addr] = Connection(client, addr, self)