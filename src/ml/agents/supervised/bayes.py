import numpy as np
from scipy.stats import multivariate_normal as mvn  # This is just the multivariate gaussian equation


class Bayes():
    def __init__(self, smoothing=1e-2, **extras):
        self.smoothing = smoothing

    def train(self, X, y):
        N, D = X.shape  # Equiv to M, N from other ML
        self.distributions = {}

        labels = set(y)
        for c in labels:
            c = int(c)
            samples_where_c = X[y == c]  # all the training examples of class c

            self.distributions[c] = {   # Distribution of features for that class
                "mean": samples_where_c.mean(axis=0),
                "cov": np.cov(samples_where_c.T) + np.eye(D) * self.smoothing,  # Covariance, smoothing prevents just 0'ing out probabilities
                "prior": len(samples_where_c) / len(y)  # Posterior = Likelihood * Prior / Scaling (Baye's Rule)
            }

    def predict(self, X):
        N, D = X.shape
        K = len(self.distributions)
        P = np.zeros((N, K))

        for c, g in self.distributions.items():
            mean, cov, prior = self.distributions[c]["mean"], self.distributions[c]["cov"], self.distributions[c]["prior"]  # Unpack values
            P[:, c] = mvn.logpdf(X, mean=mean, cov=cov) + np.log(prior)  # After a lot of debating to myself, I think some libraries are
                                                                         # a must for implementing this stuff. More in README

        return np.argmax(P, axis=1)
