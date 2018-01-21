import random
import numpy as np

from ....states.AbstractState import State
from ....ui.Plot import Plot

class ClassPlot(State):
    " The main state for this enviroment "

    def __init__(self, econfig):
        super().__init__("Classification Plot", "Environments")

        self.n = econfig.n

        self.x_range = [-10, 10]
        self.y_range = [-10, 10]

        self.params = np.zeros((econfig.n, 1))

        for i in range(econfig.n):
            self.params[i] = random.uniform(-5, 5)

        self.y = np.zeros((econfig.m, 1))
        self.x = np.zeros((econfig.m, econfig.n-1))

        i = 0
        while i < econfig.m:
            x, y = self.gen_point()
            if int(y) < self.y_range[1] and int(y) > self.y_range[0]:
                self.x[i] = x.T
                self.y[i, 0] = y
                i += 1

        self.plot = Plot(50, 50, 500, 500, self.n, self.x_range, self.y_range)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.plot.on_render(screen, self.getx()[:, 0], self.getx()[:, 1], self.gety())

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_mouse_down(self, pos):
        x_val, x_val2 = self.plot.screen_to_coords(pos)
        x = np.array([x_val, x_val2])

        if self.params.T.dot(np.insert(x, 0, 1, axis=0)) < 0:
            y = 0
        else:
            y = 1

        self.x = np.vstack((self.x, x))
        self.y = np.vstack((self.y, y))

    def gen_point(self):
        # x_val = random.uniform(self.x_range[0], self.x_range[1])
        x = np.array([random.uniform(self.x_range[0], self.x_range[1]), random.uniform(self.x_range[0], self.x_range[1])])

        if self.params.T.dot(np.insert(x, 0, 1, axis=0)) < 0:
            y = 0
        else:
            y = 1
        return x, y



    def getx(self):
        return self.x

    def gety(self):
        return self.y
