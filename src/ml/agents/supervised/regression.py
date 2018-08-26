# Copyright 2017 Andy Taylor

from math import e
import numpy as np


class Regression():
    def __init__(self, n_features, alpha=0.01):
        self.n = n_features + 1  # bias
        self.alpha = alpha

        self.params = np.zeros((self.n, 1))

        self.lambd = 9

        self.stddev = 1
        self.mean = 0

        self.num_iters = 200

    def train(self, X, y, num_iters=5000):
        m = len(y)
        if m < 2:
            return

        X = np.insert(self.scale_features(X), 0, 1, axis=1)

        self.fit(X, y, self.num_iters)

    def fit(self, X, y, num_iters):
        y = np.reshape(y, (len(y), 1))
        for i in range(num_iters):
            self.vectorized_BGD(X, y, len(y))

    def vectorized_BGD(self, X, y, m):
        self.params = np.subtract(self.params, (self.alpha * self.gradient(X, y, m)))

    def predict(self, x):
        return int(np.sum(np.insert(x, 0, 1, axis=1).dot(self.params), axis=1) > 0)

    def scale_features(self, X):
        return X


class LogisticRegression(Regression):

    def gradient(self, X, y, m):
        grad = ((np.subtract(self.sigmoid(X.dot(self.params)), y)).T.dot(X)).T

        return grad

    def cost(self, X, y, m):
        h = self.sigmoid(X.dot(self.params))
        J = (1.0 / m) * np.subtract(-(y.T).dot(np.log(h)), (1 - y).T.dot(np.log(1 - h)))

        return J

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def render_func(self, x):
        # print(x)
        return self.params.T.dot(np.insert(self.scale_features(x.T).T, 0, 1, axis=0))


class LinearRegression(Regression):

    def gradient(self, X, y, m):
        pred = X.dot(self.params)
        err = np.subtract(pred, y)

        self.params2 = np.vstack((0, self.params[1:]))
        grad = (1.0 / m) * (X.T.dot(err)) + (self.lambd / m) * self.params2

        return grad

    def cost(self, X, y, m):
        prediction = X.dot(self.params)
        err = np.subtract(prediction, y)
        J = 1.0 / (2 * m) * np.sum(np.square(err)) \
            + (self.lambd / (2 * m)) * np.sum(np.square(self.params[1:]))

        return J

    def render_func(self, x):
        # print('x', x)
        return self.params.T.dot(np.insert(self.scale_features(x.T).T, 0, 1, axis=0))
