import pygame
import numpy as np

from src import config
from .component import Component
from ..elements import *


class MainMenuButtons(Component):

    def __init__(self, x, y, w, h, screen):
        super().__init__(x, y, w, h, screen, False, config.SCHEME5)

        w = 400
        h = 100
        play_button = Button.create_rounded_button(
                        0, 0, w, h, config.BLACK, config.SCHEME2, 3,
                        "Play", config.BLACK, 62,
                        lambda: self.screen.parent.change_state("LevelSelector")
                      )

        load_button = Button.create_rounded_button(
                        0, 120, w, h, config.BLACK, config.SCHEME2, 3,
                        "Load", config.BLACK, 62,
                        lambda: print("Not Implemented")
                      )

        about_button = Button.create_rounded_button(
                        0, 240, w, h, config.BLACK, config.SCHEME2, 3,
                        "About", config.BLACK, 62,
                        lambda: print("Not Implemented")
                       )

        self.elements = [
            play_button,
            load_button,
            about_button
        ]

    def on_enter(self, data, surf):
        super().on_enter(data, surf)

    def update(self, elapsed):
        for elem in self.elements:
            elem.update(elapsed)

    def render(self, surf):
        for elem in self.elements:
            elem.render(surf)

    def has_changed(self):
        elem_changed = False
        for elem in self.elements:
            if elem.has_changed():
                elem_changed = True
                break

        return self.changed or elem_changed
