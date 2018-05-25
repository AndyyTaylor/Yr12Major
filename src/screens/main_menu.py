
import pygame
from src import config
from .screen import Screen
from ..widgets import *


class MainMenu(Screen):

    def __init__(self):
        super().__init__("MainMenu", "MasterState")

        # self.widgets.append(Label())

    def on_update(self, elapsed):
        print(int(1000 / elapsed))
