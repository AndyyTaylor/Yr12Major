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

    def step(self, action):
        return self.env.step(action)

    def on_render(self, screen):
        self.env.render()

    def get_action_space(self):
        return self.env.action_space

    def get_observation_space(self):
        return self.env.observation_space

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

    def on_mouse_event(self, event):
        pass

class MountainCar(OpenAiEnv):
    def __init__(self):
        super().__init__("CartPole-v0")

        self.num_actions = 2
        self.num_observations = 4