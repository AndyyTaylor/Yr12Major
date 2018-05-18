import pygame
import numpy as np

from src import config
from .component import Component
from ..elements import *


class Workshop(Component):

    def __init__(self, x, y, w, h, input, output, algorithms):
        super().__init__(x, y, w, h, True, config.SCHEME2)

        self.input = input
        self.output = output
        self.algorithms = [self.input, self.output] + algorithms

        self.title = Textbox(0, 0, w, 80, "Workshop", config.BLACK, 36)

        cum_y = 80
        for i, mach in enumerate(self.algorithms):
            mach.set_pos(50, cum_y)
            cum_y += 10 + mach.h

    def on_enter(self, data, surf):
        surf.fill(config.SCHEME2)

    def on_update(self, elapsed):
        for machine in self.algorithms:
            machine.on_update(elapsed)

    def _on_render(self, surf):
        for machine in self.algorithms:
            if machine.has_changed():
                machine.on_render(surf)

        if self.title.has_changed():
            self.title.on_render(surf)

        self.changed = False

    def _on_mouse_motion(self, pos):
        for machine in self.algorithms:
            machine._on_mouse_motion(np.subtract(pos, self.get_pos()))

    def has_changed(self):
        mach_changed = False
        for machine in self.algorithms:
            if machine.has_changed():
                mach_changed = True
                break

        return self.changed or mach_changed
