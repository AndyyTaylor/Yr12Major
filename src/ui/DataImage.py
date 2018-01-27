import pygame
import numpy as np

from .. import config
from .UIElement import UIElement

class DataImage(UIElement):
    def __init__(self, x, y, w, h, data_w, data_h):
        super().__init__(x, y, w, h)

        self.data_w = data_w
        self.data_h = data_h

    def on_render(self, screen, data):
        m = len(data)

        pixel_w = int(self.w / self.data_w)
        pixel_h = int(self.h / self.data_h)

        for rr in range(self.data_w):
            for cc in range(self.data_h):
                d = data[cc * self.data_w + rr]
                pygame.draw.rect(screen, (d, d, d), (self.x + rr * pixel_w, self.y + cc * pixel_h, pixel_w, pixel_h))

    def on_update(self, elapsed):
        print('data image updated')
        pass
