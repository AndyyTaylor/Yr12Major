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

    def __init__(self):
        super().__init__("Catch Apples", "Environments")

        self.num_obvs = 2
        self.grid_size = 8
        self.num_actions = 3

        self.reward = 0

        self.timer = 0
        self.max_apples = 1

    def reset(self):
        self.apples = []
        self.platform = [4, 7]
        self.lives = 3

        return self.get_obvs()

    def step(self, action):
        for i in range(len(self.apples)):
            self.apples[i][1] += 1

        self.take_action(action)
        self.check_OOB()
        self.gen_apples()
        reward = self.check_collision()

        return (self.get_obvs(), reward, self.lives <= 0, '')

    def get_obvs(self):
        closest_apple = None
        for apple in self.apples:
            if closest_apple == None or apple[1] > closest_apple[1]:
                closest_apple = apple

        if not closest_apple:
            closest_apple = [0, 0]

        return [self.platform[0], self.platform[1], closest_apple[0], closest_apple[1]]

    def take_action(self, action):
        if action == 0 and self.platform[0] > 0:
            self.platform[0] -= 1
        elif action == 2 and self.platform[0] < self.grid_size-1:
            self.platform[0] += 1

    def check_OOB(self):
        i = 0
        while i < len(self.apples):
            apple = self.apples[i]

            if apple[1] > self.grid_size:
                self.apples.remove(apple)
                self.lives -= 1
            else:
                i+=1

    def check_collision(self):
        i = 0
        reward = 0
        while i < len(self.apples):
            apple = self.apples[i]

            if apple[1] == self.platform[1] and abs(apple[0] - self.platform[0]) <= 1:
                reward += 1
                self.apples.remove(apple)
            else:
                i += 1

        return reward

    def gen_apples(self):
        while len(self.apples) < self.max_apples:
            self.apples.append([random.randint(0, self.grid_size), random.randint(0, int(self.grid_size/5))])

    def on_render(self, screen, _):
        centered_platform = self.platform[:]
        centered_platform[0] -= 1
        pygame.draw.rect(screen, config.BLACK, self.adjust_pos(tuple(centered_platform)) + (config.SCREEN_WIDTH / self.grid_size * 2.5, 30))

        for apple in self.apples:
            pygame.draw.circle(screen, config.RED, self.adjust_pos(tuple(apple)), 10)

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

    def on_update(self):
        pass

    def on_key_down(self, key):
        if key == pygame.K_LEFT and self.platform[0] > 0:
            self.platform[0] -= 1
        elif key == pygame.K_RIGHT and self.platform[0] < self.grid_size-1:
            self.platform[0] += 1

    def on_mouse_down(self, pos):
        pass
