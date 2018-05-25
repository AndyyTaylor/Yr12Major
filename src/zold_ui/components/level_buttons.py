import pygame
import numpy as np

from src import config
from .component import Component
from ..elements import *


class LevelButtons(Component):

    def __init__(self, x, y, w, h, screen, box_width, box_height, gap_size, box_border):
        super().__init__(x, y, w, h, screen, False, config.SCHEME5)

        self.box_width = box_width
        self.box_height = box_height
        self.gap_size = gap_size
        self.box_border = box_border

        self.elements = []

        self.create_level_buttons()

    def on_enter(self, data, surf):
        super().on_enter(data, surf)

    def update(self, elapsed):
        for elem in self.elements:
            elem.update(elapsed)

    def render(self, surf):
        for elem in self.elements:
            elem.render(surf)

    def create_level_buttons(self):
        level_num = 1
        for yy in range(self.y, self.y + self.h, self.box_height + self.gap_size):
            for xx in range(self.x, self.x + self.w, self.box_width + self.gap_size):
                self.create_level_button(xx, yy, level_num)
                level_num += 1

    def create_level_button(self, x, y, level_num):
        button = Button.create_rounded_button(
                    x, y, self.box_width, self.box_height,
                    config.SCHEME4, config.SCHEME3, self.box_border,
                    str(level_num), config.SCHEME1, 72,
                    lambda: self.parent.change_state("Level", level_num)
                 )

        if level_num > config.MAX_LEVEL:
            button.disable()

        self.elements.append(button)

    def has_changed(self):
        elem_changed = False
        for elem in self.elements:
            if elem.has_changed():
                elem_changed = True
                break

        return self.changed or elem_changed
