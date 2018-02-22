# Copyright 2017 Andy Taylor

from math import e, log
import numpy as np

class Regression():
    name = "Regression"

    def __init__(self, n_features, alpha=0.01):
        self.n = n_features
        self.alpha = alpha

        self.params = np.zeros((self.n, 1))

        self.stddev = 1
        self.mean = 0

    def train(self, X, y, num_iters=5000):
        m = len(y)
        if m < 2:
            return

        X = np.insert(self.scale_features(X), 0, 1, axis=1)

        self.fit(X, y, num_iters)

    def fit(self, X, y, num_iters):
        for i in range(num_iters):
            self.vectorized_BGD(X, y, len(y))

    def vectorized_BGD(self, X, y, m):
        self.params = np.subtract(self.params, (self.alpha * self.gradient(X, y, m)))

    def predict(self, x):
        # print(x)
        return self.params.T.dot(np.insert(self.scale_features(x).T, 0, 1, axis=0))

    def scale_features(self, X):
        if X.shape[0] > 1:
            self.stddev = X.std(0)
            self.mean = X.mean(0)

        return np.divide(np.subtract(X, self.mean), self.stddev)


class LogisticRegression(Regression):
    name = "Logistic Regression"

    def gradient(self, X, y, m):
        grad = ((np.subtract(self.sigmoid(X.dot(self.params)), y)).T.dot(X)).T

        return grad

    def cost(self, X, y, m):
        h = self.sigmoid(X.dot(self.params))
        J = (1.0 / m) * np.subtract(-(y.T).dot(np.log(h)), (1 - y).T.dot(np.log(1-h)))

        return J

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def render_func(self, x):
        # print(x)
        return self.params.T.dot(np.insert(self.scale_features(x.T).T, 0, 1, axis=0))


class LinearRegression(Regression):
    name = "Linear Regression"

    def gradient(self, X, y, m):
        pred = X.dot(self.params)
        err = np.subtract(pred, y)

        grad = (1.0 / m) * (X.T.dot(err))

        return grad

    def cost(self, X, y, m):
        prediction = X.dot(self.params)
        err = np.subtract(prediction, y)
        J = 1.0 / (2*m) * np.sum(np.square(err))

        return J

    def render_func(self, x):
        # print('x', x)
        return self.params.T.dot(np.insert(self.scale_features(x.T).T, 0, 1, axis=0))
