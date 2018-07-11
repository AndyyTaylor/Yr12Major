
# import pygame
#
# from src import config
from ..widgets import Component


class Output(Component):

    def __init__(self, x, y, environment):
        super().__init__(x, y, 150, 150, 'Output')

        self.environment = environment

        self.correct = 0
        self.total = 0

        self.input_pos.append((0, self.h / 2))
        self.setup_inputs_and_outputs()

    def on_update(self, elapsed):
        super().on_update(elapsed)

        holder = self.inputs[0]
        if holder.has_samples():
            sample = holder.take_sample()
            self.total += 1
            self.correct += int(self.environment.sample_correct(sample))

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        y_margin = 35
        l_x_margin = 50
        r_x_margin = 10

        width = self.w - l_x_margin - r_x_margin
        height = self.h - y_margin
        self.environment.render_correct_data(screen, (self.x + l_x_margin + int(width / 2),
                                                      self.y + y_margin + int(height / 2)),
                                             int(min(width, height) / 2))

    def get_percentage(self):
        if self.total == 0:
            return '--%'
        else:
            return str(int(self.correct / self.total * 100)) + '%'