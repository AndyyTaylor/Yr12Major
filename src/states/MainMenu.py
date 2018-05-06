" Main Menu "

import pygame
from .. import config
from .AbstractState import State
from ..ui.Rectangle import Rectangle
from ..ui.Button import Button
from ..ui.Textbox import Textbox
from ..ui import RoundedButton


class MainMenu(State):
    " A "

    def __init__(self):
        super().__init__("MainMenu", "MasterState")

        self.total_time = 0
        w = 400
        h = 100
        self.elements = [
            RoundedButton(50, 330, w, h, 3, config.BLACK, config.SCHEME2, lambda: self.parent.change_state("LevelSelector")),
            Textbox(50, 330, w, h, "Resume", config.BLACK, 62),
            RoundedButton(50, 450, w, h, 3, config.BLACK, config.SCHEME2, lambda: print("Not Implemented")),
            Textbox(50, 450, w, h, "Load", config.BLACK, 62),
            RoundedButton(40, 560, w+20, h+20, 3, config.BLACK, config.SCHEME2, lambda: print("Not Implemented")),
            Textbox(40, 560, w+20, h+20, "About", config.BLACK, 74)
        ]

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self, _):
        print("Intro state entered")

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        self.total_time += elapsed

    def on_render(self, screen):
        pygame.draw.rect(screen, config.SCHEME5, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        for elem in self.elements:
            elem.on_render(screen)

    def on_mouse_down(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for elem in self.elements:
                if isinstance(elem, Button) and pygame.Rect(elem.get_rect()).collidepoint(pos):
                    elem.on_click()
                    return
