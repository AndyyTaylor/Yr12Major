import numpy as np


class DecisionTree():
    def __init__(self):
        pass

    def entropy(self, y):
        # Entropy = E[-log(p)] = - Sigma(x) p(x) * log(p(x))
        n0 = (y == 0).sum()  # Number of class 1
        N = len(y)

        if n0 == 0 or n0 == N:  # No info to be gained from this data
            return 0

        p0 = n0 / N
        p1 = 1 - p0
        return -p0 * np.log(p0) - p1 * np.log(p1)
