import pygame

from .UIElement import UIElement

class Button(UIElement):
    def __init__(self, x, y, w, h, callback):   # pylint: disable=R0913
        super().__init__(x, y, w, h)

        self.callback = callback

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.get_rect())

    def on_click(self):
        self.callback()
