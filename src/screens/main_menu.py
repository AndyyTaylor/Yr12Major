
import pygame
from src import config
from .screen import Screen
from ..widgets import *


class MainMenu(Screen):

    def __init__(self):
        super().__init__("MainMenu", "MasterState", show_title=False, back_button=False)

        self.widgets.append(Button(50, config.SCREEN_HEIGHT - 390, 400, 100, "Play",
                            64, config.BLACK, config.BLACK, config.SCHEME2, 6,
                            lambda: self.parent.change_state("LevelSelector")))

        self.widgets.append(Button(50, config.SCREEN_HEIGHT - 270, 400, 100, "Load",
                            64, config.BLACK, config.BLACK, config.SCHEME2, 6,
                            lambda: print("Load")))  # noqa - throws bad syntax error

        self.widgets.append(Button(50, config.SCREEN_HEIGHT - 150, 400, 100, "About",
                            64, config.BLACK, config.BLACK, config.SCHEME2, 6,
                            lambda: print("About")))

    def on_update(self, elapsed):
        super().on_update(elapsed)
