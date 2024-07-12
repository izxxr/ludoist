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

from typing import TYPE_CHECKING, Any, Dict

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


def _shorten(text: str, lim: int = 15) -> str:
    if len(text) > lim:
        return text[0:lim] + "..."
    return text


position_coordinates = {
    (0, -1, -1): [(88, 88), (88, 217), (233, 217), (233, 88)],
    (1, -1, -1): [(88, 864), (233, 864), (233, 735), (88, 735)],
    (2, -1, -1): [(878, 864), (878, 735), (733, 735), (733, 863)],
    (3, -1, -1): [(877, 88), (733, 88), (733, 217), (877, 217)],
    (0, 0, 0): (571, 316),
    (0, 0, 1): (571, 253),
    (0, 0, 2): (571, 190),
    (0, 0, 3): (571, 127),
    (0, 0, 4): (571, 64),
    (0, 0, 5): (571, 2),
    (0, 1, 0): (482, 2),
    (0, 1, 1): (482, 64),
    (0, 1, 2): (482, 127),
    (0, 1, 3): (482, 190),
    (0, 1, 4): (482, 253),
    (0, 1, 5): (482, 316),
    (0, 1, 6): (482, 384),
    (0, 2, 0): (390, 2),
    (0, 2, 1): (390, 64),
    (0, 2, 2): (390, 127),
    (0, 2, 3): (390, 191),
    (0, 2, 4): (390, 253),
    (0, 2, 5): (390, 316),
    (1, 0, 0): (316, 393),
    (1, 0, 1): (253, 393),
    (1, 0, 2): (190, 393),
    (1, 0, 3): (127, 393),
    (1, 0, 4): (64, 393),
    (1, 0, 5): (2, 393),
    (1, 1, 0): (2, 482),
    (1, 1, 1): (64, 482),
    (1, 1, 2): (127, 482),
    (1, 1, 3): (190, 482),
    (1, 1, 4): (253, 482),
    (1, 1, 5): (316, 482),
    (1, 1, 6): (383, 482),
    (1, 2, 0): (2, 571),
    (1, 2, 1): (64, 571),
    (1, 2, 2): (127, 571),
    (1, 2, 3): (190, 571),
    (1, 2, 4): (253, 571),
    (1, 2, 5): (316, 571),
    (2, 0, 0): (393, 648),
    (2, 0, 1): (393, 710),
    (2, 0, 2): (393, 773),
    (2, 0, 3): (393, 836),
    (2, 0, 4): (393, 899),
    (2, 0, 5): (393, 962),
    (2, 1, 0): (482, 962),
    (2, 1, 1): (482, 899),
    (2, 1, 2): (482, 836),
    (2, 1, 3): (482, 773),
    (2, 1, 4): (482, 710),
    (2, 1, 5): (482, 648),
    (2, 1, 6): (482, 716),
    (2, 2, 0): (571, 962),
    (2, 2, 1): (571, 899),
    (2, 2, 2): (571, 836),
    (2, 2, 3): (571, 773),
    (2, 2, 4): (571, 710),
    (2, 2, 5): (571, 648),
    (3, 0, 0): (648, 571),
    (3, 0, 1): (710, 571),
    (3, 0, 2): (773, 571),
    (3, 0, 3): (836, 571),
    (3, 0, 4): (899, 571),
    (3, 0, 5): (962, 571),
    (3, 1, 0): (962, 482),
    (3, 1, 1): (899, 482),
    (3, 1, 2): (836, 482),
    (3, 1, 3): (773, 482),
    (3, 1, 4): (710, 482),
    (3, 1, 5): (648, 482),
    (3, 1, 6): (580, 482),
    (3, 2, 0): (962, 393),
    (3, 2, 1): (899, 393),
    (3, 2, 2): (836, 393),
    (3, 2, 3): (773, 393),
    (3, 2, 4): (710, 393),
    (3, 2, 5): (648, 393),
}

class MainMenu(Scene):
    """Represents the main-menu scene."""

    def __init__(self, window: LudoistWindow, state: Dict[str, Any]) -> None:
        super().__init__(window, state)

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

    def __init__(self, window: LudoistWindow, state: Dict[str, Any]) -> None:
        super().__init__(window, state)

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

    def get_name(self) -> str:
        return "settings"

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

    def __init__(self, window: LudoistWindow, state: Dict[str, Any]) -> None:
        super().__init__(window, state)

        img_button_back = self.resources.get("button_back", 70, 70)
        img_button_back_hover = self.resources.get("button_back_hover", 70, 70)
        img_button_create_game = self.resources.get("button_create_game", 70, 70)
        img_button_create_game_hover = self.resources.get("button_create_game_hover", 70, 70)

        self.window.refresh_games()
        self._games_ui = []
        self._icons = []
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
        games = self.window.games
        x = 260
        y = 550

        if len(games) == 0:
            loading_text.text = "No active games yet"
        else:
            loading_text.text = ""

        self._games_ui = []

        for game in games.values():
            if game.password_protected:
                icon_entry = self.window.resources.get("icon_locked", 50, 50)
            else:
                icon_entry = self.window.resources.get("icon_open", 50, 50)

            icon_players = self.window.resources.get("icon_players", 50, 50)
            icon_info = self.window.resources.get("icon_info", 50, 50)
            icon_info_hover = self.window.resources.get("icon_info_hover", 50, 50)

            if game.is_joinable():
                icon_join = self.window.resources.get("icon_join", 50, 50)
                icon_join_hover = self.window.resources.get("icon_join_hover", 50, 50)
            else:
                icon_join = self.window.resources.get("icon_no_join", 50, 50)
                icon_join_hover = self.window.resources.get("icon_no_join", 50, 50)

            icon_entry = pyglet.gui.PushButton(
                x=x,
                y=y,
                depressed=icon_entry,
                pressed=icon_entry,
                batch=self._batch,
            )
            icon_players = pyglet.gui.PushButton(
                x=x + 490,
                y=y + 8,
                depressed=icon_players,
                pressed=icon_players,
                batch=self._batch,
            )
            name = pyglet.text.Label(
                _shorten(game.name, lim=25),
                font_name="Poppins",
                font_size=20,
                color=(0, 0, 0, 255),
                x=x + 60,
                y=y + 17,
                bold=True,
                batch=self._batch,
            )
            players = pyglet.text.Label(
                f"{len(game.players)}/{game.rules.allowed_players}",
                font_name="Poppins",
                font_size=22,
                color=(53, 55, 67, 255),
                x=x + 550,
                y=y + 17,
                bold=True,
                batch=self._batch,
            )
            info_button = pyglet.gui.PushButton(
                x=x + 630,
                y=y + 8,
                depressed=icon_info,
                pressed=icon_info,
                hover=icon_info_hover,
                batch=self._batch,
            )
            join_button = pyglet.gui.PushButton(
                x=x + 700,
                y=y + 8,
                depressed=icon_join,
                pressed=icon_join,
                hover=icon_join_hover,
                batch=self._batch,
            )

            if game.is_joinable():
                join_button.set_handler("on_press", self._handle_join_press(game.id))

            info_button.set_handler("on_press", self._handle_info_press(game.id))
            entry = (name, players, info_button, join_button, icon_entry, icon_players)

            self._games_ui.append(entry)

            y -= 60

    def _handle_join_press(self, game_id: str):
        def _handler():
            state = {"game": self.window.games[game_id]}
            self.window.scenes.setup_scene(GameView, state)

        return _handler

    def _handle_info_press(self, game_id: str):
        def _handler():
            state = {"game": self.window.games[game_id]}
            self.window.scenes.setup_scene(GameInfo, state)

        return _handler

    def get_name(self) -> str:
        return "game_manager"

    def setup(self) -> None:
        for button in self._buttons:
            self.window.push_handlers(button)

        for entry in self._games_ui:
            self.window.push_handlers(entry[2])
            self.window.push_handlers(entry[3])

    def cleanup(self) -> None:
        for button in self._buttons:
            self.window.remove_handlers(button)

        for entry in self._games_ui:
            self.window.remove_handlers(entry[2])
            self.window.remove_handlers(entry[3])

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

    def __init__(self, window: LudoistWindow, state: Dict[str, Any]) -> None:
        super().__init__(window, state)

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
        self.window.scenes.setup_scene(GamesManager)

    def _handle_back_press(self) -> None:
        self.window.scenes.setup_scene(GamesManager)

    def get_name(self) -> str:
        return "create_game"

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


class GameInfo(Scene):
    """Information about a game."""
    def __init__(self, window: LudoistWindow, state: Dict[str, Any]) -> None:
        super().__init__(window, state)

        self._game = g = state["game"]

        img_button_back = self.resources.get("button_back", 50, 50)
        img_button_back_hover = self.resources.get("button_back_hover", 50, 50)
        icon_players = self.resources.get("icon_players", 50, 50)
        icon_security = self.resources.get("icon_locked" if g.password_protected else "icon_open", 50, 50)
        icon_info = self.resources.get("icon_info", 50, 50)

        self._batch = pyglet.graphics.Batch()
        self._labels = [
            create_heading(_shorten(self._game.name), window, self._batch),
        ]
        self._widgets = [
            pyglet.gui.PushButton(x=(window.width - img_button_back.width) // 2, y=350,
                                  depressed=img_button_back, pressed=img_button_back,
                                  hover=img_button_back_hover, batch=self._batch),
        ]
        self._widgets[0].set_handler("on_press", self._handle_back_press)
        self._info_components = []
        self._info_y = 620
        self._add_info("Room Name", _shorten(g.name, 25), icon_info)
        self._add_info("Allowed Players", str(g.rules.allowed_players), icon_players)
        self._add_info("Players Joined", str(len(g.players)), icon_players)
        self._add_info("Join Security", "Password" if g.password_protected else "Open", icon_security)

    def _handle_back_press(self) -> None:
        self.window.scenes.setup_scene(GamesManager)

    def _add_info(self, option: str, value: str, icon: Any):
        obj = pyglet.gui.PushButton(
            x=self.window.width // 2 - 270,
            y=self._info_y - 25,
            depressed=icon,
            pressed=icon,
            batch=self._batch,
        )
        self._info_components.append(obj)
        obj = pyglet.text.Label(
            option + ":",
            font_name="Poppins",
            font_size=24,
            bold=True,
            batch=self._batch,
            anchor_x="center",
            anchor_y="center",
            align="center",
            color=(53, 55, 67, 255),
            x=self.window.width // 2 - 50,
            y=self._info_y,
        )
        self._info_components.append(obj)
        obj = pyglet.text.Label(
            value,
            font_name="Poppins",
            font_size=24,
            batch=self._batch,
            anchor_y="center",
            color=(53, 55, 67, 255),
            x=self.window.width // 2 + 130,
            y=self._info_y,
        )
        self._info_components.append(obj)
        self._info_y -= 50

    def get_name(self) -> str:
        return "game_info"

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


class GameView(Scene):
    """The main game."""
    def __init__(self, window: LudoistWindow, state: Dict[str, Any]) -> None:
        super().__init__(window, state)

    def get_name(self) -> str:
        return "game_view"

    def setup(self) -> None:
        ...

    def cleanup(self) -> None:
        ...

    def draw(self) -> None:
        background = self.resources.get("ludo_board")
        background.blit(0, 0)
