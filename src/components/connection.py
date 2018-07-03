
import pygame
import numpy as np

from src import config
from ..widgets.widget import Widget


class Connection(Widget):

    def __init__(self, in_holder, out_holder):
        super().__init__(0, 0, 0, 0, None, 'connection')

        self.in_holder = in_holder
        self.out_holder = out_holder

        self.data = []

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, None)

        # So we need to get the 'global' pos by assigning a parent to each widget
        # also somehow this needs to cause re-renders
        start_pos = self.in_holder.get_global_center() if self.in_holder else pygame.mouse.get_pos()
        end_pos = self.out_holder.get_global_center() if self.out_holder else pygame.mouse.get_pos()

        pygame.draw.line(screen, config.BLACK, start_pos, end_pos, 3)
        self.changed = True

        self.x, self.y = start_pos
        self.w, self.h = np.subtract(end_pos, start_pos)

        if self.w < 0:
            self.w *= -1
            self.x = self.x - self.w
        if self.h < 0:
            self.h *= -1
            self.y = self.y - self.h
