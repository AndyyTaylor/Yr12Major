import random
import numpy as np

from ....states.AbstractState import State
from ....ui.Plot import Plot

class LinearPlot(State):
    " The main state for this enviroment "

    def __init__(self, m, n):
        super().__init__("LinearData", "Environments")

        self.n = n

        self.x_range = [-30, 30]
        self.y_range = [-100, 100]

        self.params = np.zeros((n, 1))

        for i in range(n):
            self.params[i] = random.uniform(-2, 2)

        self.y = np.zeros((m, 1))
        self.x = np.zeros((m, n-1))

        i = 0
        while i < m:
            x, y = self.gen_point()
            if y < self.y_range[1] and y > self.y_range[0]:
                self.x[i] = x.T
                self.y[i, 0] = y
                i += 1



        self.plot = Plot(50, 50, 500, 500, self.n, self.x_range, self.y_range)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen, agent):
        self.plot.on_render(screen, self.getx()[:, 0], self.gety()[:, 0])
        self.plot.renderFunction(screen, agent.predict)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_mouse_down(self, pos):
        x_val, y = self.plot.screen_to_coords(pos)
        x = np.array([(x_val**(i+1)) for i in range(self.n-1)])

        self.x = np.vstack((self.x, x))
        self.y = np.vstack((self.y, y))

    def gen_point(self):
        x_val = random.uniform(self.x_range[0], self.x_range[1])
        x = np.array([(x_val**(i+1)) for i in range(self.n-1)])

        y = self.params.T.dot(np.insert(x, 0, 1, axis=0)) + np.random.normal(0, 1, 1)[0]
        return x, y

    def getx(self):
        return self.x

    def gety(self):
        return self.y
