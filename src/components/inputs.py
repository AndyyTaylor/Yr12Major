
import pygame
import numpy as np
from .component import Component
from .component import Holder
from .. import config
from ..ui.Textbox import Textbox


class ColorInput(Component):

    def __init__(self, num_colors):
        super().__init__(0, 0, 200, 150)
        self.text = Textbox(self.x, self.y, self.w, 40, "Colour", config.SCHEME1, 32)

        self.colors = [config.RED, config.GREEN, config.BLUE, config.YELLOW, config.WHITE][:num_colors]

        self.output_pos.append((self.x + self.w - self.slot_width, self.y + self.h/2 - self.slot_height/2))

        self.setup_inputs_and_outputs()

    def on_render(self, screen):
        super().on_render(screen)

        row_width = 110/1.2
        num_rows = int(np.sqrt(len(self.colors)))+1

        for yy in range(num_rows):
            for xx in range(num_rows):

                if yy * np.floor(num_rows) + xx >= len(self.colors):
                    break

                color = self.colors[int(yy * np.floor(num_rows) + xx)]

                pygame.draw.rect(screen, color, (self.x+20+(row_width*1.2//num_rows)*xx, self.y+40+(row_width*1.2//num_rows)*yy, (row_width//num_rows), (row_width//num_rows)))

        self.text.on_render(screen)
