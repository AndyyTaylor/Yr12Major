" Main Menu "

import pygame
from .. import config
from .AbstractState import State
from ..ui.Rectangle import Rectangle
from ..ui.Button import Button
from ..ui.Textbox import Textbox

class MainMenu(State):
    " A "

    def __init__(self):
        super().__init__("Main", "Menu")

        self.total_time = 0
        self.elements = [
            Textbox(100, 10, 400, 50, "What would you like to see today?", config.BLACK, 32),
            Button(50, 80, 500, 110,
                   config.BLACK, config.WHITE,
                   "Supervised", config.BLACK, 42,
                   lambda: self.parent.change_state("Environments")),
            Button(50, 210, 500, 110,
                   config.BLACK, config.WHITE,
                   "Unsupervised", config.BLACK, 42,
                   lambda: self.parent.change_state("Environments")),
            Button(50, 340, 500, 110,
                   config.BLACK, config.WHITE,
                   "Reinforcement", config.BLACK, 42,
                   lambda: self.parent.change_state("Environments")),
            Button(50, 470, 235, 110,
                   config.BLACK, config.WHITE,
                   "", config.BLACK, 42,
                   lambda: self.parent.change_state("Environments")),
            Button(315, 470, 235, 110,
                   config.BLACK, config.WHITE,
                   "", config.BLACK, 42,
                   lambda: self.parent.change_state("Environments"))
        ]

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        print("Intro state entered")

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        self.total_time += elapsed

    def on_render(self, screen):
        for elem in self.elements:
            elem.on_render(screen)

    def on_mouse_down(self, pos):
        for elem in self.elements:
            if isinstance(elem, Button) and pygame.Rect(elem.get_rect()).collidepoint(pos):
                elem.on_click()
                return
