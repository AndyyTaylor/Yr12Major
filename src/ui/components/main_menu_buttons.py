import pygame
import numpy as np

from src import config
from .component import Component
from ..elements import *


class MainMenuButtons(Component):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, False, config.SCHEME2)

    def on_enter(self, data, surf):
        surf.fill(config.SCHEME2)

    def on_update(self, elapsed):
        for machine in self.algorithms:
            machine.on_update(elapsed)

    def on_render(self, surf):
        super().on_render(surf)
        # for machine in self.algorithms:
        #     if machine.has_changed():
        #         machine.on_render(surf)
        #
        # if self.title.has_changed():
            # self.title.on_render(surf)

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
