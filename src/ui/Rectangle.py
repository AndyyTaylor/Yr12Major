import pygame

from .UIElement import UIElement

class Rectangle(UIElement):
    def __init__(self, x, y, w, h, color):  # pylint: disable=R0913
        super().__init__(x, y, w, h)

        self.color = color

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())
