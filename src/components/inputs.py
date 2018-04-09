
import pygame
from .component import Component
from .. import config
from ..ui.Textbox import Textbox


class ColorInput(Component):
    def __init__(self, num_colors):
        super().__init__(0, 0, 200, 150)

        self.text = Textbox(self.x, self.y, self.w, 40, "Colour", config.SCHEME1, 32)

    def on_render(self, screen):
        self.draw_rounded_rect(screen, self.get_rect(), config.SCHEME4)

        self.text.on_render(screen)
        pygame.draw.rect(screen, config.SCHEME3, (self.x + self.w - self.slot_width
                                                  , self.y + self.h/2 - self.slot_height/2
                                                  , self.slot_width, self.slot_height))
