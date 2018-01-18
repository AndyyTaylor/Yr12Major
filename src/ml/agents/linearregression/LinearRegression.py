
import numpy as np

class LinearRegression():

    def __init__(self):
        self.params = np.zeros(2)
        self.params[1] = 1

    def on_update(self, points):
        self.BGD(points)

    def on_render(self, screen, plot):
        plot.renderFunction(screen, self.func)

    def func(self, x):
        return self.params[1] * x + self.params[0]

    def BGD(self, points):
        bgrad = 1.0/len(points) * sum([self.func(points[i].getX()) - points[i].getY() for i in range(len(points))])
        mgrad = 1.0/len(points) * sum([(self.func(points[i].getX()) - points[i].getY()) * points[i].getX() for i in range(len(points))])

        self.params[0] -= 0.05 * bgrad
        self.params[1] -= 0.05 * mgrad
