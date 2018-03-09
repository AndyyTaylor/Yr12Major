import numpy as np


class Bayes():
    def __init__(self, smoothing=1e-2, **extras):
        self.smoothing = smoothing

    def train(self, X, y):
        N, D = X.shape  # Equiv to M, N from other ML
        self.distributions = {}

        labels = set(y)
        for c in labels:
            samples_where_c = X[y == c]  # all the training examples of class c

            self.distributions[c] = {
                "mean": samples_where_c.mean(axis=0),
                "cov": np.cov(samples_where_c.T) + np.eye(D) * self.smoothing,
                "prior": len(samples_where_c) / len(y)
            }

    def predict(self, X):
        N, D = X.shape
        K = len(self.distributions)
        P = np.zeros((N, K))

        for c, g in self.distributions.items():
            mean, cov, prior = self.distributions[c]["mean"], self.distributions[c]["cov"], self.distributions[c]["prior"]
            P[: , c] =
