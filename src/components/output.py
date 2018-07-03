
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

    def get_percentage(self):
        if self.total == 0:
            return '--%'
        else:
            return str(int(self.correct / self.total * 100)) + '%'
