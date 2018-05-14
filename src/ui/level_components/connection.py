
import pygame
import numpy as np
from .algorithms import Algorithm
from ..uielement import UIElement
from src import config


class Connection(UIElement):

    def __init__(self, in_holder, out_holder, render_data):
        self.in_holder = in_holder
        self.out_holder = out_holder
        self.render_data = render_data

        self.data = []

    def on_update(self, elapsed):
        if (not self.data or not isinstance(self.out_holder.component, Algorithm)) and self.in_holder.has_data():
            sample = self.in_holder.take_data()
            sample.progress = 0
            self.data.append(sample)

        out_comp = self.out_holder.component
        if hasattr(out_comp, 'get_avg_cool_down'):
            travel_time = out_comp.get_avg_cool_down()
        else:
            travel_time = 1000

        data_clone = self.data[:]
        for sample in self.data:
            sample.progress += 1 * (elapsed / travel_time)
            if sample.progress >= 1:
                self.out_holder.add_data(sample)
                data_clone.remove(sample)

        self.data = data_clone

    def on_render(self, screen):
        pygame.draw.line(screen, config.GREEN, self.in_holder.get_center(), self.out_holder.get_center(), 5)

        start_pos = self.in_holder.get_center()
        end_pos = self.out_holder.get_center()
        travel = tuple(np.subtract(end_pos, start_pos))
        for sample in self.data:
            pos = tuple(np.add(start_pos, np.multiply(travel, sample.progress)))
            self.render_data(screen, int(pos[0]), int(pos[1]), self.data[0])

    def has_data(self):
        return len(self.data) > 0  # This could be implicit, but this is more readable

    def on_mouse_motion(self, pos):
        pass

    def on_mouse_down(self, pos):
        pass

    def on_mouse_up(self, pos):
        pass
