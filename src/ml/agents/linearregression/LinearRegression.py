
import numpy as np

class LinearRegression():

    def __init__(self):
        self.params = np.zeros(2)
        self.params[1] = 1

    def on_update(self):
        pass

    def on_render(self, screen, plot):
        plot.renderFunction(screen, self.func)

    def func(self, x):
        return self.params[1] * x + self.params[0]
