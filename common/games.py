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

from oblate import Schema, fields
from common import fields as _fields
from common.enums import GameState, PieceColor

import uuid
import random

__all__ = (
    "Game",
    "GamePlayer",
    "GameRules",
)


class GamePlayer(Schema):
    """A player in the game."""

    id = fields.String(default=lambda *_: str(uuid.uuid4()))
    """The player's unique ID."""

    token = fields.String(default=None, none=True)
    """The authentication token used by the player to interact in the game."""

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

    def is_joinable(self):
        """Whether the game can be joined."""
        return len(self.players) < self.rules.allowed_players and self.state in (GameState.ready, GameState.waiting)

    def get_overview(self):
        """Returns the overview of the game."""
        players = [p.get_public_view() for p in self.players]
        data = self.dump(exclude=["password", "players"])
        data["players"] = players
        data["password_protected"] = self.password is not None
        return data