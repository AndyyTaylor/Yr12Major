
import pygame
import numpy as np

from src import config
from ..widgets.widget import Widget


class Connection(Widget):

    def __init__(self, in_holder, out_holder, render_data):
        super().__init__(0, 0, 0, 0, None, 'connection')

        self.in_holder = in_holder
        self.out_holder = out_holder
        self.render_data = render_data

        self.speed = 1

        self.prev_scroll = None

        self.samples = []

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if self.in_holder is not None and self.out_holder is not None:
            self.collect_samples()
            self.progress_samples(elapsed)

            if self.in_holder.parent.parent is not None:  # Component is being dragged
                current_scroll = self.in_holder.parent.parent.get_scroll()
                if current_scroll != self.prev_scroll:
                    self.prev_scroll = current_scroll
                    self.rebuild_pos()

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, None)

        start_pos, end_pos = self.rebuild_pos()

        pygame.draw.line(screen, config.BLACK, start_pos, end_pos, 3)

        pos_diff = np.subtract(end_pos, start_pos)
        for sample in self.samples:
            diff = np.multiply(pos_diff, sample.progress)
            pos = np.add(start_pos, diff)
            self.render_data(screen, sample.y, tuple([int(x) for x in pos]))

        self.changed = True

    def collect_samples(self):
        if self.in_holder.has_samples() and len(self.samples) < 1:
            self.samples.append(self.in_holder.take_sample())

    def progress_samples(self, elapsed):
        for sample in self.samples:
            sample.progress += min((elapsed / 1000) * self.speed, 1 - sample.progress)

            if sample.progress == 1:
                self.out_holder.add_sample(sample)
                self.samples.remove(sample)

    def rebuild_pos(self):
        start_pos = self.in_holder.get_global_center() if self.in_holder else pygame.mouse.get_pos()
        end_pos = self.out_holder.get_global_center() if self.out_holder else pygame.mouse.get_pos()

        self.x, self.y = start_pos
        self.w, self.h = np.subtract(end_pos, start_pos)

        if self.w < 0:
            self.w *= -1
            self.x = self.x - self.w
        if self.h < 0:
            self.h *= -1
            self.y = self.y - self.h

        return start_pos, end_pos

    def clear_samples(self):
        self.samples = []
