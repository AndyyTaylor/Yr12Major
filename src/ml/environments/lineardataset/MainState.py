import random
import numpy as np

from ....states.AbstractState import State
from ..utility.DataHandler import DataHandler
from ....ui.Plot import Plot

class MainState(State):
    " The main state for this enviroment "

    def __init__(self):
        super().__init__("LinearData", "Environments")

        self.x_range = [0, 1]
        self.y_range = [0, 1]

        self.params = [random.uniform(self.y_range[0], self.y_range[1]),
                       random.uniform(-1, 1)]

        self.data_hander = DataHandler(self.gen_point, 100)
        self.plot = Plot(50, 50, 500, 500, self.x_range, self.y_range)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.plot.on_render(screen, self.data_hander.get_points())

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_mouse_down(self, pos):
        pass

    def gen_point(self):
        # x = random.uniform(self.x_range[0], self.x_range[1])
        # y = random.uniform(self.y_range[0], self.y_range[1])
        x = random.uniform(self.x_range[0], self.x_range[1])
        y = self.params[1] * x + self.params[0] + np.random.normal(0, 0.05, 1)[0]
        return x, y
