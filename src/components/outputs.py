
import pygame
from .component import Component
from .. import config
from ..ui.Textbox import Textbox


class ColorOutput(Component):
    def __init__(self, num_colors):
        super().__init__(0, 0, 200, 150)

        self.text = Textbox(self.x, self.y, self.w, 40, "OUT", config.SCHEME1, 32)

        self.input_pos.append((self.x, self.y + self.h/2 - self.slot_height/2))

        self.setup_inputs_and_outputs()

    def on_render(self, screen):
        super().on_render(screen)

        self.text.on_render(screen)
