
import numpy as np

class LinearRegression():

    def __init__(self):
        self.params = np.zeros((2, 1))
        self.params[0] = 1

    def on_update(self, points):
        X = np.zeros((len(points), 2))
        y = np.zeros((len(points), 1))

        for i in range(len(points)):
            X[i, 0] = 1
            X[i, 1] = points[i].getX()

        for i in range(len(points)):
            y[i, 0] = points[i].getY()

        self.vectorizedBGD(X, y)
        # self.BGD(points)

    def on_render(self, screen, plot):
        plot.renderFunction(screen, self.func)

    def func(self, x):
        return self.params[1] * x + self.params[0]

    def BGD(self, points):
        bgrad = 1.0/len(points) * sum([self.func(points[i].getX()) - points[i].getY() for i in range(len(points))])
        mgrad = 1.0/len(points) * sum([(self.func(points[i].getX()) - points[i].getY()) * points[i].getX() for i in range(len(points))])

        self.params[0] -= 0.2 * bgrad
        self.params[1] -= 0.2 * mgrad

    def vectorizedBGD(self, X, y):
        pred = X.dot(self.params)

        err = np.square(np.subtract(pred, y))
        J = 1.0 / (2*len(y)) * np.sum(err)

        print(J)

        alpha = 0.2
        new_params = np.subtract(self.params, (alpha / len(y)) * (X.T.dot(np.subtract(pred, y))))

        self.params = new_params
