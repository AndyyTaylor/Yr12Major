
import pygame
from .component import Component
from .. import config
from ..ui.Textbox import Textbox


class ColorOutput(Component):
    def __init__(self, num_colors, render_data):
        super().__init__(0, 0, 200, 150, False)

        self.render_data = render_data

        self.text = Textbox(self.x, self.y, self.w, 40, "OUT", config.SCHEME1, 32)

        self.input_pos.append((self.x, self.y + self.h/2 - self.slot_height/2))
        self.input_labels.append(0)

        self.correct = 0
        self.total = 0

        self.setup_inputs_and_outputs()

    def on_update(self, elapsed):
        in_holder = self.inputs[0]
        if in_holder.has_data():
            sample = in_holder.take_data()
            if sample.y == 0:
                self.correct += 1
            self.total += 1

    def on_render(self, screen):
        super().on_render(screen)

        if self.total > 0:
            perc = Textbox(self.x, self.y + 50, self.w, 40, str(int(self.correct / self.total * 100)) + "%", config.SCHEME1, 32)
            perc.on_render(screen)
        self.text.on_render(screen)


class Trash(Component):

    def __init__(self):
        super().__init__(0, 0, 200, 150)
        self.text = Textbox(self.x, self.y, self.w, 40, "TRASH", config.SCHEME1, 32)

        self.input_pos.append((self.x, self.y + self.h/2 - self.slot_height/2))
        self.setup_inputs_and_outputs()

    def on_render(self, screen):
        super().on_render(screen)

        self.text.on_render(screen)
