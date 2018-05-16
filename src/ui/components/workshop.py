import pygame

from src import config
from .component import Component
from ..elements import *


class Workshop(Component):

    def __init__(self, x, y, w, h, input, output, algorithms):
        super().__init__(x, y, w, h, True)

        self.input = input
        self.output = output
        self.algorithms = [self.input, self.output] + algorithms

        self.title = Textbox(0, 0, w, 80, "Workshop", config.BLACK, 36)

        cum_y = 80
        for i, mach in enumerate(self.algorithms):
            mach.set_pos(50, cum_y)
            cum_y += 10 + mach.h

    def on_update(self, elapsed):
        for machine in self.algorithms:
            machine.on_update(elapsed)

    def _on_render(self, surf):
        surf.fill(config.SCHEME2)

        for machine in self.algorithms:
            machine.on_render(surf)

        self.title.on_render(surf)
