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

from typing import TYPE_CHECKING, Any

from client.scenes_manager import Scene
from client.widgets import StateAwareToggle

import pyglet
import random

if TYPE_CHECKING:
    from client.window import LudoistWindow

__all__ = (
    "MainMenu",
)


def create_heading(text: str, window: LudoistWindow, batch: pyglet.graphics.Batch):
    rect = pyglet.shapes.Rectangle(
        x=window.width // 2 - 200,
        y=680,
        width=400,
        height=100,
        color=(53, 55, 67, 150),
        batch=batch,
    )
    label = pyglet.text.Label(
        text,
        font_name="Poppins",
        font_size=26,
        bold=True,
        stretch=True,
        batch=batch,
        anchor_x="center",
        anchor_y="center",
        align="center",
        x=window.width // 2,
        y=730,
    )
    return rect, label


class MainMenu(Scene):
    """Represents the main-menu scene."""

    def __init__(self, window: LudoistWindow) -> None:
        super().__init__(window)

        img_button_play = self.resources.get("button_play")
        img_button_play_clicked = self.resources.get("button_play_clicked")
        img_button_play_hover = self.resources.get("button_play_hover")
        img_button_settings = self.resources.get("button_settings", 60, 60)
        img_button_settings_hover = self.resources.get("button_settings_hover", 60, 60)
        img_button_exit = self.resources.get("button_exit", 60, 60)
        img_button_exit_hover = self.resources.get("button_exit_hover", 60, 60)

        self._batch = pyglet.graphics.Batch()
        self._buttons = [
            pyglet.gui.PushButton(x=(self.window.width - img_button_play.width) // 2,
                                  y=(self.window.height - img_button_play.height) // 2,
                                  depressed=img_button_play, pressed=img_button_play_clicked,
                                  hover=img_button_play_hover, batch=self._batch),

            pyglet.gui.PushButton(x=(self.window.width - img_button_settings.width) // 2 - 55,
                                  y=(self.window.height - img_button_settings.height) // 2 - 120,
                                  depressed=img_button_settings, pressed=img_button_settings,
                                  hover=img_button_settings_hover, batch=self._batch),

            pyglet.gui.PushButton(x=(self.window.width - img_button_exit.width) // 2 + 55,
                                  y=(self.window.height - img_button_exit.height) // 2 - 120,
                                  depressed=img_button_exit, pressed=img_button_exit,
                                  hover=img_button_exit_hover, batch=self._batch),
        ]

        self._buttons[0].set_handler("on_press", self._handle_play_press)
        self._buttons[1].set_handler("on_press", self._handle_settings_press)
        self._buttons[2].set_handler("on_press", self._handle_exit_press)

    def get_name(self) -> str:
        return "main_menu"

    def _handle_exit_press(self) -> None:
        self.window.close()
        self.window.on_close()

    def _handle_play_press(self) -> None:
        self.window.scenes.setup_scene(GamesManager)

    def _handle_settings_press(self) -> None:
        self.window.scenes.setup_scene(Settings)

    def setup(self) -> None:
        for button in self._buttons:
            self.window.push_handlers(button)

    def cleanup(self) -> None:
        for button in self._buttons:
            self.window.remove_handlers(button)

    def draw(self) -> None:
        background = self.resources.get("background_main_menu")
        background.blit(0, 0)
        self._batch.draw()


class Settings(Scene):
    """Represents the settings menu scene."""

    # this needs to be a class variable to ensure that
    # the restart message persists between scene transitions
    _show_restart_message = False

    def __init__(self, window: LudoistWindow) -> None:
        super().__init__(window)

        self._batch = pyglet.graphics.Batch()
        self._settings_objects = []
        self._settings_y = 620
        self._shapes = [
            pyglet.shapes.Rectangle(x=self.window.width // 2 - 275, y=250, width=550,
                                    height=100, color=(255, 0, 0, 80), batch=self._batch),
        ]
        self._labels = [
            create_heading("Display Settings", window, self._batch),
            pyglet.text.Label("Restart is needed for changes to apply.", font_name="Poppins",
                              font_size=20, bold=True, stretch=True, batch=self._batch,
                              anchor_x="center", anchor_y="center", align="center",
                              x=self.window.width // 2, y=300)
        ]
        self._labels[1].visible = self.__class__._show_restart_message
        self._shapes[0].visible = self.__class__._show_restart_message
        self._add_toggle_setting("Fullscreen", self._handle_fullscreen, self.window.cfg.fullscreen)
        self._draw_back_button()

    def _add_toggle_setting(self, text: str, handler: Any, value: bool):
        img_button_on = self.resources.get("button_on", 70, 70)
        img_button_off = self.resources.get("button_off", 70, 70)
        obj = pyglet.text.Label(
            text,
            font_name="Poppins",
            font_size=24,
            bold=True,
            batch=self._batch,
            anchor_x="center",
            anchor_y="center",
            align="center",
            color=(53, 55, 67, 255),
            x=self.window.width // 2 - 100,
            y=self._settings_y,
        )
        self._settings_objects.append(obj)
        obj = StateAwareToggle(
            x=750,
            y=self._settings_y - 36,
            depressed=img_button_off,
            pressed=img_button_on,
            batch=self._batch,
            toggled=self.window.cfg.fullscreen,
        )
        obj.set_handler("on_toggle", handler)
        self._settings_objects.append(obj)
        self._settings_y -= 50

    def _handle_fullscreen(self, value: bool) -> None:
        self.window.cfg.update({"fullscreen": value})
        self.__class__._show_restart_message = new = not self.__class__._show_restart_message
        self._labels[1].visible = new
        self._shapes[0].visible = new

    def _draw_back_button(self) -> None:
        img_button_back = self.resources.get("button_back", 70, 70)
        img_button_back_hover = self.resources.get("button_back_hover", 70, 70)

        self._button_back = pyglet.gui.PushButton(
            x=(self.window.width - img_button_back.width) // 2,
            y=self._settings_y - 100,
            depressed=img_button_back,
            pressed=img_button_back,
            hover=img_button_back_hover,
            batch=self._batch,
        )
        self._button_back.set_handler("on_press", self._handle_back_press)

    def _handle_back_press(self) -> None:
        self.window.scenes.setup_scene(MainMenu)

    def setup(self) -> None:
        for item in self._settings_objects:
            if isinstance(item, pyglet.gui.WidgetBase):
                self.window.push_handlers(item)

        self.window.push_handlers(self._button_back)

    def cleanup(self) -> None:
        for item in self._settings_objects:
            if isinstance(item, pyglet.gui.WidgetBase):
                self.window.remove_handlers(item)

        self.window.remove_handlers(self._button_back)

    def draw(self) -> None:
        background = self.resources.get("background_main_menu")
        background.blit(0, 0)

        self._batch.draw()


class GamesManager(Scene):
    """The games manager menu showing all the ongoing games."""

    def __init__(self, window: LudoistWindow) -> None:
        super().__init__(window)

        img_button_back = self.resources.get("button_back", 70, 70)
        img_button_back_hover = self.resources.get("button_back_hover", 70, 70)
        img_button_create_game = self.resources.get("button_create_game", 70, 70)
        img_button_create_game_hover = self.resources.get("button_create_game_hover", 70, 70)

        self._games_ui = []
        self._batch = pyglet.graphics.Batch()
        self._shapes = [
            pyglet.shapes.Box(x=(window.width - 800) // 2, y=180, width=800, height=450,
                              color=(53, 55, 67, 255), thickness=3, batch=self._batch),
        ]
        self._labels = [
            create_heading("Active Games", window, self._batch),
            pyglet.text.Label("", font_name="Poppins", font_size=18, bold=True,
                              color=(53, 55, 67, 255), batch=self._batch,
                              x=window.width - 380, y=650),

            pyglet.text.Label("", font_name="Poppins", font_size=18, bold=True,
                              color=(53, 55, 67, 150), batch=self._batch, anchor_x="center",
                              align="center", x=self.window.width // 2, y=550),
        ]
        self._buttons = [
            pyglet.gui.PushButton(x=(window.width - img_button_back.width) // 2 - 40, y=80,
                                  depressed=img_button_back, pressed=img_button_back,
                                  hover=img_button_back_hover, batch=self._batch),

            pyglet.gui.PushButton(x=((window.width - img_button_create_game.width) // 2) + 40,
                                  y=80, depressed=img_button_create_game, pressed=img_button_create_game,
                                  hover=img_button_create_game_hover, batch=self._batch),
        ]

        self._populate_games()
        self._buttons[0].set_handler("on_press", self._handle_back_press)
        self._buttons[1].set_handler("on_press", self._handle_create_game_press)

    def _handle_create_game_press(self) -> None:
        self.window.scenes.setup_scene(CreateGame)

    def _handle_back_press(self) -> None:
        self.window.scenes.setup_scene(MainMenu)

    def _populate_games(self) -> None:
        loading_text = self._labels[2]
        if len(self.window.games) == 0:
            loading_text.text = "No active games yet"
        else:
            loading_text.text = f"{len(self.window.games)} games available"

    def setup(self) -> None:
        for button in self._buttons:
            self.window.push_handlers(button)

    def cleanup(self) -> None:
        for button in self._buttons:
            self.window.remove_handlers(button)

    def draw(self) -> None:
        background = self.resources.get("background_main_menu")
        background.blit(0, 0)

        lat = self.window.connection.latency
        ping = 0 if lat == -1 else round(lat * 1000)
        self._labels[1].text = f"Ping: {ping}ms"

        if ping >= 0 and ping < 30:
            color = (50, 168, 82, 255)
        elif ping > 30 and ping < 100:
            color = (180, 245, 2, 255)
        elif ping > 100 and ping < 200:
            color = (255, 89, 0, 255)
        else:
            color = (255, 0, 0, 255)

        self._labels[1].color = color
        self._batch.draw()


class CreateGame(Scene):
    """Game creation screen."""

    def __init__(self, window: LudoistWindow) -> None:
        super().__init__(window)

        img_button_back = self.resources.get("button_back", 70, 70)
        img_button_back_hover = self.resources.get("button_back_hover", 70, 70)
        img_button_create_game = self.resources.get("button_create_game", 70, 70)
        img_button_create_game_hover = self.resources.get("button_create_game_hover", 70, 70)

        self._batch = pyglet.graphics.Batch()
        self._labels = [
            create_heading("Create Game", window, self._batch),
            pyglet.text.Label("Room Name", font_name="Poppins", font_size=24, bold=True,
                              batch=self._batch, anchor_x="center", anchor_y="center",
                              align="center", color=(53, 55, 67, 255),
                              x=self.window.width // 2 - 200, y=595),
        ]
        self._widgets = [
            pyglet.gui.TextEntry(f"Ludo Match {random.randint(1000, 9999)}",
                                 x=self.window.width // 2 - 50, y=570, width=350,
                                 batch=self._batch),

            pyglet.gui.PushButton(x=(window.width - img_button_back.width) // 2 - 40, y=450,
                                  depressed=img_button_back, pressed=img_button_back,
                                  hover=img_button_back_hover, batch=self._batch),

            pyglet.gui.PushButton(x=((window.width - img_button_create_game.width) // 2) + 40,
                                  y=450, depressed=img_button_create_game, pressed=img_button_create_game,
                                  hover=img_button_create_game_hover, batch=self._batch),
        ]
        t = self._widgets[0]
        t._pad = 4
        t.height = 50
        t._doc.set_style(0, len(t._doc.text), dict(font_size=24))

        self._widgets[1].set_handler("on_press", self._handle_back_press)
        self._widgets[2].set_handler("on_press", self._handle_create_game_press)

    def _handle_create_game_press(self) -> None:
        self.window.connection.create_game(name=self._widgets[0].value)
        self.window.refresh_games()
        self.window.scenes.setup_scene(GamesManager)

    def _handle_back_press(self) -> None:
        self.window.scenes.setup_scene(GamesManager)

    def setup(self) -> None:
        for widget in self._widgets:
            self.window.push_handlers(widget)

    def cleanup(self) -> None:
        for widget in self._widgets:
            self.window.remove_handlers(widget)

    def draw(self) -> None:
        background = self.resources.get("background_main_menu")
        background.blit(0, 0)
        self._batch.draw()

