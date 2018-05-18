" Main Menu "

import pygame
from .screen import Screen
from ..elements import *
from ..components import *
from src import config


class MainMenu(Screen):
    " A "

    def __init__(self):
        super().__init__("MainMenu", "MasterState")

        # Button w & h
        w = 400
        h = 100
        play_button = Button.create_rounded_button(
                        50, 470, w, h, config.BLACK, config.SCHEME2, 3,
                        "Play", config.BLACK, 62,
                        lambda: self.parent.change_state("LevelSelector")
                      )

        load_button = Button.create_rounded_button(
                        50, 590, w, h, config.BLACK, config.SCHEME2, 3,
                        "Load", config.BLACK, 62,
                        lambda: print("Not Implemented")
                      )

        about_button = Button.create_rounded_button(
                        50, 710, w, h, config.BLACK, config.SCHEME2, 3,
                        "About", config.BLACK, 62,
                        lambda: print("Not Implemented")
                       )

        self.components = [
            play_button,
            load_button,
            about_button
        ]
