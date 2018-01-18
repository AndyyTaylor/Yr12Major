import random
import numpy as np

from ....states.AbstractState import State
from ....ui.Plot import Plot

class MainState(State):
    " The main state for this enviroment "

    def __init__(self, econfig):
        super().__init__("LinearData", "Environments")

        self.x_range = [0, 1.5]
        self.y_range = [0, 2]

        self.params = np.zeros((econfig.n, 1))

        for i in range(econfig.n):
            self.params[i] = random.uniform(0, 1)

        self.y = np.zeros((econfig.m, 1))
        self.x = np.zeros((econfig.m, econfig.n-1))

        for i in range(100):
            x, y = self.gen_point()
            self.x[i] = x.T
            self.y[i, 0] = y



        self.plot = Plot(50, 50, 500, 500, self.x_range, self.y_range)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.plot.on_render(screen, self.getx(), self.gety())

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
        x_val = random.uniform(self.x_range[0], self.x_range[1])
        x = np.array([[x_val], [x_val**2]])

        y = self.params.T.dot(np.insert(x, 0, 1, axis=0))
        return x, y

    def getx(self):
        return self.x

    def gety(self):
        return self.y
