
import numpy as np
from .environment import Environment


class ShapeEnv(Environment):

    def __init__(self, num_shapes, num_samples=100):
        shapes = [[0], [1], [2], [3], [4]]

        self.X = np.zeros((num_samples, 3))
        self.y = np.zeros(num_samples)

        for i in range(num_samples):
            self.X[i] = np.array(shapes[int(i // (num_samples / num_shapes))])
            self.y[i] = int(i // (num_samples / num_shapes))

        self.create_train_cross_test(self.X, self.y, 0.7, 0.7)
