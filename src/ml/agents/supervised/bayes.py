import numpy as np


class Bayes():
    def __init__(self, smoothing=1e-2, **extras):
        self.smoothing = smoothing

    def train(self, X, y):
        N, D = X.shape  # Equiv to M, N from other ML
        self.gaussians = {}
        self.priors = {}
        labels = set(y)

        for c in labels:
            current_x = X[y == c]  # all the training examples of class c
            self.gaussians[c] = {
                'mean': current_x.mean(axis=0),
                'cov': np.cov(current_x.T) + np.eye(D) * self.smoothing  # covariance, smoothing prevents probabilities being 0
            }                                                            # which is problematic since they're multiplied later
            self.priors[c] = len(y[y == c]) / len(y)

    def predict(self, X):
        return 0
