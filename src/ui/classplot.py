import pygame
import numpy as np
from .. import config


class ClassPlot():
    def __init__(self, num_classes):
        self.colors = [config.RED, config.BLUE]

        self.scale = 200

        if len(self.colors) < num_classes:
            raise NotImplementedError("ClassPlot doesn't have enough colors")

    def render(self, screen, X, Y, predict):
        pred = predict(X)

        for m in range(len(Y)):
            x, y = X[m, :]
            if Y[m] == pred[m]:
                pygame.draw.circle(screen, self.colors[Y[m]], (int(x * self.scale), int(y * self.scale)), 5)
            else:
                pygame.draw.circle(screen, config.BLACK, (int(x * self.scale), int(y * self.scale)), 5)
