import pygame

from src import config
from ..uielement import UIElement


class Rectangle(UIElement):

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)

        self.color = color

    def on_render(self, screen, animation_progress=0):
        pygame.draw.rect(screen, self.color, self.get_rect())