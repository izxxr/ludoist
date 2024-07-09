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

from typing import Type, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client.window import LudoistWindow

__all__ = (
    "ScenesManager",
)


class Scene:
    """Abstract class for describing a specific scene in-game."""

    def __init__(self, window: LudoistWindow):
        self.window = window
        self.resources = window.resources

    def get_name(self) -> str:
        """Returns the scene name."""
        raise NotImplementedError

    def setup(self) -> None:
        """Sets up the scene.

        This method is mainly used as a pre-initialization hook
        that gets called when the scene has initially started.
        """
        raise NotImplementedError

    def cleanup(self) -> None:
        """Gracefully cleans up the scene.

        This method is called when the scene is being removed.
        """
        raise NotImplementedError

    def draw(self) -> None:
        """Draw the scene."""
        raise NotImplementedError


class ScenesManager:
    """The scenes manager.

    This class manages transitions between different scenes.
    """
    def __init__(self, window: LudoistWindow) -> None:
        self._window = window
        self._block_draw = False
        self._current_scene = None

    def get_current_scene(self) -> Optional[Scene]:
        return self._current_scene

    def draw_current_scene(self) -> None:
        if self._block_draw:
            return

        if self._current_scene is None:
            raise RuntimeError("no scene to draw")

        self._current_scene.draw()

    def setup_scene(self, scene: Type[Scene]) -> None:
        if self._current_scene:
            self._current_scene.cleanup()

        self._current_scene = scene(self._window)
        self._current_scene.setup()
