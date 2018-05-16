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

        self.total_time = 0
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

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self, _, screen):
        super().on_enter(_, screen)

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        super().on_update(elapsed)

    def on_render(self, screen):
        super().on_render(screen)

    def on_mouse_down(self, event, pos):
        for comp in self.components:
            if isinstance(comp, Button) and pygame.Rect(comp.get_rect()).collidepoint(pos):
                comp.on_click()
                return

    def on_mouse_up(self, event, pos):
        pass
