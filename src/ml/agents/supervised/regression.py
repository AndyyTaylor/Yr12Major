# Copyright 2017 Andy Taylor

from math import e, log
import numpy as np

class Regression():
    def __init__(self, n_features, alpha=0.01, lam=1):
        self.n = n_features
        self.alpha = alpha
        self.lam = lam

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
        return self.params.T.dot(np.insert(self.scale_features(x).T, 0, 1, axis=0))

    def scale_features(self, X):
        if X.shape[0] > 1:
            self.stddev = X.std(0)
            self.mean = X.mean(0)

        return np.divide(np.subtract(X, self.mean), self.stddev)

    def cost(self, X, y, m):
        return self._cost(X, y, m) + self.regularization(m)

    def gradient(self, X, y, m):
        return self._gradient(X, y, m) + self.regularization_grad(m)

    def regularization(self, m):
        params2 = np.copy(self.params)
        params2[0] = 0
        return (self.lam / (2 * m)) * np.sum(np.power(params2, 2))

    def regularization_grad(self, m):
        params2 = np.copy(self.params)
        params2[0] = 0
        return (self.lam / m) * np.sum(params2)

    def render_func(self, x):
        return self.params.T.dot(np.insert(self.scale_features(x.T).T, 0, 1, axis=0))


class LogisticRegression(Regression):

    def _gradient(self, X, y, m):
        grad = ((np.subtract(self.sigmoid(X.dot(self.params)), y)).T.dot(X)).T

        return grad

    def _cost(self, X, y, m):
        h = self.sigmoid(X.dot(self.params))
        J = (1.0 / m) * np.subtract(-(y.T).dot(np.log(h)), (1 - y).T.dot(np.log(1-h)))

        return J

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

class LinearRegression(Regression):

    def _gradient(self, X, y, m):
        pred = X.dot(self.params)
        err = np.subtract(pred, y)

        grad = (1.0 / m) * (X.T.dot(err))

        return grad

    def _cost(self, X, y, m):
        prediction = X.dot(self.params)
        err = np.subtract(prediction, y)
        J = 1.0 / (2*m) * np.sum(np.square(err))

        return J
