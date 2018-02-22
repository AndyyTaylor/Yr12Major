" Main Menu "

import pygame
from .. import config
from .AbstractState import State
from ..ui.Rectangle import Rectangle
from ..ui.Button import Button
from ..ui.Textbox import Textbox


class Selection(State):
    def __init__(self, tier1="agent", tier2="supervised"):
        super().__init__("Selection", "Menu")

        self.elements = []

        if tier1 == "agent" and tier2 == "supervised":
            from ..ml.agents.supervised import all_classes
            for i in range(len(all_classes)):
                agent = all_classes[i]
                self.elements.append(Textbox(100, 10 + 60*i, 400, 50, agent.name, config.BLACK, 32))

    def on_render(self, screen):
        for elem in self.elements:
            elem.on_render(screen)

    def on_mouse_down(self, pos):
        for elem in self.elements:
            if isinstance(elem, Button) and pygame.Rect(elem.get_rect()).collidepoint(pos):
                elem.on_click()
                return
