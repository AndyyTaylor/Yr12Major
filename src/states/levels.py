
from ..components import *


class Level():
    def __init__(self, level_num):
        self.input = None
        self.output = None

        self.load_level(level_num)

    def load_level(self, level_num):
        if level_num == 1:
            self.input = ColorInput(2)
            self.output = ColorOutput(2)
