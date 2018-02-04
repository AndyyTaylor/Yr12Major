import gym
import random
import pygame
import numpy as np

from .... import config
from ....states.AbstractState import State

class OpenAiEnv(State):
    " The main state for this enviroment "

    def __init__(self, name):
        super().__init__("OpenAiEnv", "Environments")

        self.env = gym.make(name)

    def reset(self):
        return self.env.reset()

    def on_render(self, screen):
        pass

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
        pass

    def on_mouse_down(self, pos):
        pass

class Pendulum(OpenAiEnv):
    def __init__(self):
        super().__init__("Pendulum-v0")
        # print(self.env.action_space.shape)
        self.num_actions = 2