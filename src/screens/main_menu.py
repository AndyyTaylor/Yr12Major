
import pygame
from src import config
from .screen import Screen
from ..widgets import *


class MainMenu(Screen):

    def __init__(self):
        super().__init__("MainMenu", "MasterState")

        self.widgets.append(Label(0, 0, config.SCREEN_WIDTH, 150, config.SCHEME2, "Main Menu", 118, config.BLACK))
        self.widgets.append(Button(100, config.SCREEN_HEIGHT - 300, 200, 100, "Play", 64, config.BLACK, config.BLACK, config.SCHEME2, 6))

    def on_update(self, elapsed):
        super().on_update(elapsed)

        print(int(1000 / elapsed))
