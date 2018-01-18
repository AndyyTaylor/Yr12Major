
import numpy as np

class LinearRegression():

    def __init__(self, econfig):
        self.m = econfig.m
        self.n = econfig.n

        self.params = np.zeros((self.n, 1))
        self.params[0] = 1

    def on_update(self, x, y):

        X = np.insert(x, 0, 1, axis=1)

        self.vectorizedBGD(X, y)
        # self.BGD(points)

    def on_render(self, screen, plot):
        plot.renderFunction(screen, self.func)

    def func(self, x):
        return self.params.T.dot(np.insert(x, 0, 1, axis=0))

    def vectorizedBGD(self, X, y):
        pred = X.dot(self.params)

        err = np.square(np.subtract(pred, y))
        J = 1.0 / (2*self.m) * np.sum(err)

        print(J)
        print((X.T.dot(np.subtract(pred, y))).shape)

        alpha = 0.5
        new_params = np.subtract(self.params, (alpha / self.m) * (X.T.dot(np.subtract(pred, y))))
        self.params = new_params










    def BGD(self, points):
        bgrad = 1.0/len(points) * sum([self.func(points[i].getX()) - points[i].getY() for i in range(len(points))])
        mgrad = 1.0/len(points) * sum([(self.func(points[i].getX()) - points[i].getY()) * points[i].getX() for i in range(len(points))])

        self.params[0] -= 0.2 * bgrad
        self.params[1] -= 0.2 * mgrad
