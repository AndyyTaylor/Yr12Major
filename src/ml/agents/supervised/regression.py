# Copyright 2017 Andy Taylor

import numpy as np

class LinearRegression():
    def __init__(self, n_features, alpha=0.01):
        self.n = n_features
        self.alpha = alpha

        self.params = np.zeros((self.n, 1)) # Random?

        self.stddev = 1
        self.mean = 0

    def on_update(self, X, y):
        self.vectorized_BGD(np.insert(self.scale_features(X), 0, 1, axis=1), y)

    def vectorized_BGD(self, X, y, num_iters=1000):
        m = len(y)
        if m < 2:
            return

        for i in range(num_iters):
            prediction = X.dot(self.params)
            err = np.subtract(prediction, y)
            J = 1.0 / (2*m) * np.sum(np.square(err))

            # print(J)

            new_params = np.subtract(self.params, (self.alpha / m) * (X.T.dot(err)))
            self.params = new_params


    # Regression class ?
    def scale_features(self, X):
        if X.shape[0] > 1:
            self.stddev = X.std(0)
            self.mean = X.mean(0)

        return np.divide(np.subtract(X, self.mean), self.stddev)

    def on_render(self, screen, plot):
        plot.renderFunction(screen, self.render_func)

    def render_func(self, x):
        return self.params.T.dot(np.insert(self.scale_features(x.T).T, 0, 1, axis=0))
