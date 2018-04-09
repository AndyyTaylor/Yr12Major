" Andy "
from .AbstractState import State

import pygame

from .. import config


class Level(State):
    " A "

    def __init__(self):
        super().__init__("Level", "MasterState")

    def on_enter(self, data):
        print("Level " + str(data) + " entered")

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        screen.fill(config.SCHEME5)
        pygame.draw.rect(screen, config.SCHEME2, (0, 0, 300, config.SCREEN_HEIGHT))
        pygame.draw.rect(screen, config.SCHEME4, (50, 50, 200, 200))

    def on_mouse_down(self, pos):
        pass
