
import pygame
from src import config
from .screen import Screen
from ..widgets import *


class LevelSelector(Screen):

    def __init__(self):
        super().__init__("LevelSelector", "MasterState")

        self.widgets.append(Label(0, 0, config.SCREEN_WIDTH, 150, config.SCHEME2, "Level Selector", 118, config.BLACK))
        self.widgets.append(Button(100, config.SCREEN_HEIGHT - 300, 200, 100, "Play", 64, config.BLACK, config.BLACK, config.SCHEME2, 6, lambda: self.parent.change_state("LevelSelector")))

    def on_update(self, elapsed):
        super().on_update(elapsed)

        print(int(1000 / elapsed))
