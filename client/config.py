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

from typing import Dict, Any

import json

__all__ = (
    "Configuration",
)


class Configuration:
    """Reads and manages configuration of client."""

    def __init__(self, filename: str):
        self._filename = filename
        self.refresh()

    def refresh(self) -> None:
        """Refresh the configuration."""
        with open(self._filename, "r") as f:
            cfg = json.load(f)

        self._config = cfg
        self._assign_attrs()

    def _assign_attrs(self):
        self.fullscreen = self._config.get("fullscreen", True)

    def update(self, data: Dict[str, Any]) -> None:
        self._config.update(data)
        self._assign_attrs()

        with open(self._filename, "w") as f:
            json.dump(self._config, f, indent=4)
