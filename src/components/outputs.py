
# import pygame
#
# from src import config
from ..widgets import Component


class Output(Component):

    def __init__(self, x, y):
        super().__init__(x, y, 150, 150, 'Output')

        self.input_pos.append((0, self.h / 2))

        self.setup_inputs_and_outputs()
