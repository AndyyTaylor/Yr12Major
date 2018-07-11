
import pygame
import numpy as np


class Environment():
    def __init__(self, target_y):
        self.target_y = target_y

    def create_train_cross_test(self, X, y, train_perc, cross_perc):
        m = X.shape[0]

        X, y = self.unison_shuffled_copies(X, y)

        self.trainX = X[:int(np.floor(m * train_perc)), :]
        self.trainy = y[:int(np.floor(m * train_perc))]

        self.crossX = X[int(np.ceil(m * train_perc)):int(np.floor(m * cross_perc)), :]
        self.crossy = y[int(np.ceil(m * train_perc)):int(np.floor(m * cross_perc))]

        self.testX = X[int(np.ceil(m * cross_perc)):, :]
        self.testy = y[int(np.ceil(m * cross_perc)):]

        self.labels = np.array(tuple(set(y)))

    def get_labels(self):
        return self.labels

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    def on_render(self, screen):
        pass

    def render_correct_data(self, screen, pos, size=10):
        self.render_data(screen, self.target_y, pos, size)

    def render_data(self, screen, data, pos, size=10):
        pygame.draw.circle(screen, (255, 255, 0), pos, size)

    def sample_correct(self, sample):
        if sample.y == self.target_y:
            return True

        return False
