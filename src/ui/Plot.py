import pygame
import numpy as np

from .. import config
from .UIElement import UIElement

class Plot(UIElement):
    def __init__(self, x, y, w, h, n, x_range, y_range): # pylint: disable=R0913
        super().__init__(x, y, w, h)

        self.x_range = x_range
        self.y_range = y_range

        self.n = n

    def on_update(self, elapsed):
        pass

    def on_render(self, screen, vec_x, vec_y):
        pygame.draw.rect(screen, config.GRAY, self.get_rect())

        for i in range(len(vec_y)):
            x, y = self.adjust((vec_x[i, 0], vec_y[i, 0]))
            if x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.h:
                pygame.draw.circle(screen, config.BLUE, (x, y), 2)

    def adjust(self, point):
        x, y = point

        x = (x - self.x_range[0]) * (self.w / (self.x_range[1] - self.x_range[0])) + self.x
        y = (y - self.y_range[0]) * (self.w / (self.y_range[1] - self.y_range[0])) + self.y
        return int(x), int(y)

    def screen_to_coords(self, point):
        x, y = point

        x = (x - self.x) * ((self.x_range[1] - self.x_range[0]) / self.w) + self.x_range[0]
        y = (y - self.y) * ((self.y_range[1] - self.y_range[0]) / self.w) + self.y_range[0]
        return x, y

    def renderFunction(self, screen, func):
        prev_point = None
        for xx in self.frange(self.x_range[0], self.x_range[1], 0.1):
            arr = [] # [[xx], [xx**2], [xx**3]]
            for i in range(self.n-1):
                arr.append([xx**(i+1)])

            new_point = self.adjust((xx, func(np.array(arr))))

            if prev_point:
                pygame.draw.line(screen, config.RED, prev_point, new_point)

            prev_point = new_point

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step
