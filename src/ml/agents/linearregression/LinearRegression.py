
import numpy as np

class LinearRegression():

    def __init__(self, econfig):
        self.n = econfig.n

        self.params = np.zeros((self.n, 1))
        self.params[0] = 1

        self.scale = False

        # self.scale = scale  # np.array([20, 20**2, 20**3])

    def on_update(self, x, y):
        if len(x) < 2: return
        self.scale = x.std(0)

        X = np.insert(np.divide(x, self.scale), 0, 1, axis=1)
        # print(X)
        self.vectorizedBGD(X, y)
        # self.BGD(points)

    def on_render(self, screen, plot):
        plot.renderFunction(screen, self.func)

    def func(self, x):
        if type(self.scale) == bool:
            return 0

        y = self.params.T.dot(np.insert(np.divide(x.T, self.scale).T, 0, 1, axis=0))

        return y

    def vectorizedBGD(self, X, y):
        for iter in range(200):
            pred = X.dot(self.params)

            err = np.square(np.subtract(pred, y))
            J = 1.0 / (2*len(y)) * np.sum(err)

            # print(J)
            if J > 10**36:
                print("ALPHA TOO BIG")

            # print((self.params).shape)
            alpha = 0.01
            # print(X)
            # print("---------")
            # print(self.params)
            # print(X.T.dot(np.subtract(pred, y)))
            new_params = np.subtract(self.params, (alpha / len(y)) * (X.T.dot(np.subtract(pred, y))))
            self.params = new_params

            # print(self.params)









    def BGD(self, points):
        bgrad = 1.0/len(points) * sum([self.func(points[i].getX()) - points[i].getY() for i in range(len(points))])
        mgrad = 1.0/len(points) * sum([(self.func(points[i].getX()) - points[i].getY()) * points[i].getX() for i in range(len(points))])

        self.params[0] -= 0.2 * bgrad
        self.params[1] -= 0.2 * mgrad
