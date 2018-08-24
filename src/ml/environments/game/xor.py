
import pygame
import numpy as np
from .environment import Environment
from src import config


class XOREnv(Environment):
    def __init__(self, target_y=0, num_samples=2000):
        super().__init__(target_y, num_samples)

        self.num_features = 2

        self.X = []
        self.y = []

        self.x_origin = 1.5
        self.y_origin = 1.5

        for i in range(self.num_samples):
            x = np.random.random()
            y = np.random.random()
            self.X.append([x, y])

            if not (np.round(x) == np.round(y)):
                self.y.append(0)
            else:
                self.y.append(1)

        self.X = np.array(self.X)
        self.y = np.array(self.y)

        self.create_train_cross_test(self.X, self.y, config.TRAIN_PERC, config.TRAIN_PERC)

    def render_data(self, screen, data, pos, size=10):
        if data == 0:
            color = config.BLUE
        else:
            color = config.RED
        pygame.draw.circle(screen, color, pos, size)
