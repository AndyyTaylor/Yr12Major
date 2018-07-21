
import pygame
import numpy as np

from src import config
from .environment import Environment


class ColorEnv(Environment):

    def __init__(self, num_colors, target_y=0, num_samples=100):
        super().__init__(target_y, num_samples)

        self.colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 1]]

        self.X = np.zeros((self.num_samples, 3))
        self.y = np.zeros(self.num_samples)

        for i in range(self.num_samples):
            self.X[i] = np.array(self.colors[int(i // (self.num_samples / num_colors))])
            self.y[i] = int(i // (self.num_samples / num_colors))

        self.create_train_cross_test(self.X, self.y, config.TRAIN_PERC, config.TRAIN_PERC)

    def render_data(self, screen, data, pos, size=10):
        pygame.draw.circle(screen, np.multiply(self.colors[int(data)], 255), pos, size)
