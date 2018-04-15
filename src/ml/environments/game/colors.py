
import numpy as np


class ColorEnv():

    def __init__(self, num_colors, num_samples=10):
        colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 1]]

        self.X = np.zeros((num_samples, 3))
        self.y = np.zeros(num_samples)

        for i in range(num_samples):
            self.X[i] = np.array(colors[int(i // (num_samples / num_colors))])
            self.y[i] = int(i // (num_samples / num_colors))
