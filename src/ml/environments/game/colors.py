
import pygame
import numpy as np

from .environment import Environment


class ColorEnv(Environment):

    def __init__(self, num_colors, target_y=0, num_samples=100):
        super().__init__(target_y)

        self.colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 1]]

        self.X = np.zeros((num_samples, 3))
        self.y = np.zeros(num_samples)

        for i in range(num_samples):
            self.X[i] = np.array(self.colors[int(i // (num_samples / num_colors))])
            self.y[i] = int(i // (num_samples / num_colors))

        self.create_train_cross_test(self.X, self.y, 0.7, 0.7)

    def render_data(self, screen, data, pos):
        pygame.draw.circle(screen, np.multiply(self.colors[int(data)], 255), pos, 10)
