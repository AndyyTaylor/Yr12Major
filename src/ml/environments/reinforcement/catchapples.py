import random
import os
import struct
import pygame
import numpy as np

from .... import config
from ....states.AbstractState import State
from ....ui.DataImage import DataImage
from ....ui.Textbox import Textbox
from ....ui.Button import Button

class CatchApples(State):
    " The main state for this enviroment "

    def __init__(self, agent):
        super().__init__("Catch Apples", "Environments")

        self.agent = agent

        self.num_obvs = 2
        self.grid_size = 20

        self.x = np.zeros((1, self.num_obvs))
        self.reward = 0

        self.apples = [[5.5, 1.5], [10.5, 3.5]]
        self.platform = [0, 18]

        self.timer = 0

    def on_update(self, elapsed):
        self.timer += elapsed

        if self.timer > 1000:
            self.timer -= 1000
            for i in range(len(self.apples)):
                self.apples[i][1] += 1

    def on_render(self, screen):
        pygame.draw.rect(screen, config.BLACK, self.adjust_pos(tuple(self.platform)) + (config.SCREEN_WIDTH / self.grid_size, 30))

        for apple in self.apples:
            pygame.draw.circle(screen, config.BLACK, self.adjust_pos(tuple(apple)), 10)

    def adjust_pos(self, pos):
        x, y = pos
        x = config.SCREEN_WIDTH / self.grid_size * x
        y = config.SCREEN_HEIGHT / self.grid_size * y
        return (int(x), int(y))

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_key_down(self, key):
        if key == pygame.K_LEFT and self.platform[0] > 0:
            self.platform[0] -= 1
        elif key == pygame.K_RIGHT and self.platform[0] < self.grid_size-1:
            self.platform[0] += 1

    def on_mouse_down(self, pos):
        pass

    def getx(self):
        return self.x

    def gety(self):
        return self.y
