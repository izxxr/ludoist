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

from typing import List
from oblate import Schema, fields, validate
from common import fields as _fields
from common.enums import GameState, PieceColor

import uuid
import random

__all__ = (
    "Game",
    "GamePlayer",
    "GameRules",
)


INITIAL_BOARD = [[[-1, -1] for _ in range(4)] for __ in range(4)]


class GamePlayer(Schema):
    """A player in the game."""

    id = fields.String(default=lambda *_: str(uuid.uuid4()))
    """The player's unique ID."""

    token = fields.String(default=None, none=True)
    """The authentication token used by the player to interact in the game."""

    owner = fields.Boolean(default=False)
    """Whether this player created the game."""

    name = fields.String(default=lambda *_: f"Ludo Match {random.randint(1000, 9999)}")
    """The name of player."""

    piece_color = _fields.IntEnumField(PieceColor, default=None)
    """The color of piece player is controlling."""

    def get_public_view(self):
        """Returns public view of player excluding authentication details."""
        return self.dump(exclude=["token"])


class GameRules(Schema):
    """The rules for a game."""

    allowed_players = fields.Literal(2, 3, 4, default=2)
    """Number of allowed maximum players in the game."""


class Game(Schema):
    """Represents an ongoing game."""

    id = fields.String(default=lambda *_: str(uuid.uuid4()))
    """The game's unique ID."""

    password = fields.String(default=None, none=True)
    """The password required to join this game."""

    name = fields.String(default=lambda *_: f"Ludo Match {random.randint(1000, 9999)}")
    """The name of this game."""

    state = _fields.IntEnumField(GameState, default=GameState.waiting)
    """The current state of the game."""

    rules = fields.Object(GameRules, default=lambda *_: GameRules({}))
    """The rules for this game."""

    players = _fields.SchemaList(GamePlayer)
    """The list of players in the game."""

    board = fields.List(List[List[int]], validators=[validate.Length(exact=4)], default=INITIAL_BOARD)
    """List positions of pieces on board for each color.

    This list will have four nested lists. Each nested list
    will have four further nested lists representing the positions.

    The indexes of this list will respect the PieceColor enum. That is,
    nested list at first index would always be for red color, second for
    green color and so on.

    For example::

        [
            [
                [-1, -1], [2, 3], [1, 2], [0, 1]
            ],
            ... (three more similar lists)
        ]

    In this example, the red pieces are at positions (-1, -1) (yard), (2, 3),
    (1, 2), (0, 1).

    For information on how individual piece positions are represented and
    interpreted, see the following gist:

    https://gist.github.com/izxxr/dfb75f6aa4440faf1c948d37942385fd
    """

    password_protected = fields.Boolean(default=None)
    """Whether the game is protected by password (only in overviews)"""

    def is_joinable(self):
        """Whether the game can be joined."""
        return len(self.players) < self.rules.allowed_players and self.state in (GameState.ready, GameState.waiting)

    def is_overview(self):
        """Whether this object is an overview instead of complete game data."""
        return self.password_protected is not None

    def get_overview(self):
        """Returns the overview of the game."""
        players = [p.get_public_view() for p in self.players]
        data = self.dump(exclude=["password", "players", "board"])
        data["players"] = players
        data["password_protected"] = self.password is not None
        return data
