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

from client.resource_manager import ResourceManager
from client.scenes_manager import ScenesManager
from client.config import Configuration
from client import scenes

import pyglet

__all__ = (
    "LudoistWindow",
)


class LudoistWindow(pyglet.window.Window):
    """The Ludoist client window."""

    def __init__(self) -> None:
        self.cfg = Configuration("config.json")

        super().__init__(
            width=1280,
            height=1024,
            fullscreen=self.cfg.fullscreen,
        )

        self.resources = ResourceManager("resources", self)
        self.scenes = ScenesManager(self)
        self.scenes.setup_scene(scenes.MainMenu)

    def on_draw(self):
        self.clear()
        self.scenes.draw_current_scene()
