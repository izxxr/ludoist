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

import pyglet

__all__ = (
    "StateAwareToggle",
)

# This is a slight modification of pyglet.gui.ToggleButton
# As the built-in toggle button does not allow changing the initial
# state of the button.
# https://github.com/pyglet/pyglet/pull/1158
class StateAwareToggle(pyglet.gui.PushButton):
    def __init__(self, toggled=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._sprite.image = self._pressed_img if toggled else self._depressed_img
        self._pressed = toggled

    def _get_release_image(self, x, y):
        return self._hover_img if self._check_hit(x, y) else self._depressed_img

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.enabled or not self._check_hit(x, y):
            return
        self._pressed = not self._pressed
        self._sprite.image = self._pressed_img if self._pressed else self._get_release_image(x, y)
        self.dispatch_event('on_toggle', self._pressed)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or self._pressed:
            return
        self._sprite.image = self._get_release_image(x, y)

    def on_toggle(self, value: bool):
        """Event: returns True or False to indicate the current state."""


StateAwareToggle.register_event_type('on_toggle')

