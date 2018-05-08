
import pygame
from ..ui.UIElement import UIElement
from ..ui import *
from .. import config
from .component import Component
from src.ml.agents import *


class KNN(Component):

    def __init__(self):
        super().__init__(0, 0, 200, 150)

        self.text = Textbox(self.x, self.y, self.w, 40, "KNN", config.SCHEME1, 32)
        self.algorithm = ClassificationKNN()

        self.input_pos.append((self.x, self.y + self.h/2 - self.slot_height/2))
        self.output_pos.append((self.x + self.w - self.slot_width, self.y + self.h/2 - self.slot_height/2))

        self.setup_inputs_and_outputs()

    def on_render(self, screen):
        super().on_render(screen)

        self.text.on_render(screen)

    def on_update(self, elapsed):
        super().on_update(elapsed)

        in_holder = self.inputs[0]
        out_holder = self.outputs[0]
        if in_holder.has_data():
            out_holder.add_data(in_holder.take_data())
