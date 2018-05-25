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

        self.components.append(MainMenuButtons(50, 470, 800, 700, self))
