
import pygame
from src import config
from .screen import Screen
from ..widgets import *
from ..components import *


class Level(Screen):

    def __init__(self):
        super().__init__('Level', 'MasterState', back_screen='LevelSelector')

        self.component_frame = Frame(0, 220, 300, config.SCREEN_HEIGHT - 160, True, config.SCHEME2)
        # component_frame.add_child()
        self.widgets.append(self.component_frame)

        self.widgets.append(Label(0, 160, 300, 60, config.SCHEME2, "Components", 36, config.BLACK))

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

        print("Entering level", data)

        self.component_frame.add_child(ColorInput(10, 10, 3))

    def on_update(self, elapsed):
        super().on_update(elapsed)
