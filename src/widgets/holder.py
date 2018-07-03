
import pygame

from src import config
from .widget import Widget


class Holder(Widget):

    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, config.SCHEME3, 'holder', parent=parent)

        self.data = []

        self.hover = False
        self.clicked = False

        self.alphaCover = pygame.Surface((self.w, self.h))
        self.alphaCover.set_alpha(128)
        self.alphaCover.fill(config.WHITE)

        self.prev_hash = None

    def on_update(self, elapsed):
        new_hash = hash((self.hover))

        if new_hash != self.prev_hash:
            self.changed = True
            self.prev_hash = new_hash

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        pygame.draw.rect(screen, config.SCHEME3, self.get_rect())

        if self.hover:
            screen.blit(self.alphaCover, self.get_pos())

        self.changed = False

    def on_mouse_motion(self, pos):
        self.hover = pygame.Rect(self.get_rect()).collidepoint(pos)
