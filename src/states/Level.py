" Andy "
from .AbstractState import State

import pygame

from .levels import Level
from .. import config
from ..components import *


class LevelState(State):
    " A "

    def __init__(self):
        super().__init__("Level", "MasterState")

        self.components = []

    def on_enter(self, data):
        print("Level " + str(data) + " entered")

        self.level = Level(data)
        self.components.append(self.level.input)
        self.components.append(self.level.output)

        cum_y = 0
        for i in range(len(self.components)):
            self.components[i].set_pos(50, 50 + cum_y)
            cum_y += 50 + self.components[i].h

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        screen.fill(config.SCHEME5)
        pygame.draw.rect(screen, config.SCHEME2, (0, 0, 300, config.SCREEN_HEIGHT))

        for comp in self.components:
            comp.on_render(screen)

    def on_mouse_down(self, event, pos):
        for component in self.components:
            component.on_mouse_down(pos)

    def on_mouse_motion(self, event, pos):
        for component in self.components:
            component.on_mouse_motion(pos)

    def on_mouse_up(self, event, pos):
        for component in self.components:
            component.on_mouse_up(pos)
