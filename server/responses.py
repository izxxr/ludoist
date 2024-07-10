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

from typing import Any

__all__ = (
    "OP_CODE_ERROR",
    "OP_CODE_HELLO",
    "OP_CODE_PONG",
    "OP_CODE_LIST_GAMES",
    "OP_CODE_PING",
    "OP_CODE_REQUEST_GAMES",
    "ERR_UNKNOWN_ERROR",
    "ERR_UNPARSABLE_DATA",
    "ERR_INVALID_DATA_FORMAT",
    "ERR_GAMES_LISTING_FAILED",
    "make_hello_message",
    "make_error_message",
)

# OP code range sent by server: 0-19
OP_CODE_ERROR = 0
OP_CODE_HELLO = 1
OP_CODE_PONG  = 2
OP_CODE_LIST_GAMES  = 3

# OP code range sent by client: 20-39
OP_CODE_PING = 20
OP_CODE_REQUEST_GAMES = 21

# Error codes
ERR_UNKNOWN_ERROR = 1000
ERR_PING_TIMEOUT  = 1001
ERR_UNPARSABLE_DATA = 1002
ERR_INVALID_DATA_FORMAT  = 1003
ERR_GAMES_LISTING_FAILED = 1004


def _make_message(op_code: int, data: Any = None):
    msg = {"op": op_code, "d": data}
    if data is not None:
        msg["d"] = data
    return msg


def make_hello_message(ping_interval: int):
    return _make_message(OP_CODE_HELLO, {"ping_interval": ping_interval})

def make_error_message(error_code: int, message: str):
    return _make_message(OP_CODE_ERROR, {"message": message})

def make_pong_message():
    return _make_message(OP_CODE_PONG)
