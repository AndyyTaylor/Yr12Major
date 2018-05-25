import pygame

from src import config
from ..basicelement import BasicElement


class Rectangle(BasicElement):

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)

        self.color = color

    def render(self, screen, animation_progress=0):
        pygame.draw.rect(screen, self.color, self.get_rect())
