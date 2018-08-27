import pandas as pd
import numpy as np
import pygame

from src import config
from .environment import Environment


class DigitRecognition(Environment):
    def __init__(self, num_samples=20, train_samples=1000):
        super().__init__(0, num_samples)

        self.X, self.y = self.get_data(train_samples + num_samples)

        perc = (train_samples) / (num_samples + train_samples)
        self.create_train_cross_test(self.X, self.y, perc, perc)

        self.num_features = self.X.shape[1]

        self.font = pygame.font.Font('data/fonts/Square.ttf', 18)

    def get_data(self, limit=None):
        df = pd.read_csv("data/datasets/digit-recognition/train.csv")
        data = df.as_matrix()

        np.random.shuffle(data)

        # first column is the labels
        X = data[:, 1:] / 255.0  # scale data
        y = data[:, 0]

        if limit is not None:
            X = X[:limit]
            y = y[:limit]

        return X, y

    def render_data(self, screen, data, pos, size=10):
        rendered = self.font.render(str(data), True, config.BLACK)
        screen.blit(rendered, pos)
