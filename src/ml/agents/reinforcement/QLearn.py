import random
import numpy as np

class QLearn():
    def __init__(self, num_observations, num_actions, **kwargs):
        self.num_actions = num_actions
        self.num_observations = num_observations

        self.load_keyword_args(kwargs)

    def choose_action(self, state):
        if random.random() > self.epsilon:
            # TODO: choose actual action
            return random.randint(self.num_actions)

        return random.randint(self.num_actions)

    def load_keyword_args(self, kwargs):
        if 'alpha' in kwargs: self.alpha = kwargs['alpha']
        else: self.alpha = 0.05

        if 'gamma' in kwargs: self.gamma = kwargs['gamma']
        else: self.gamma = 0.05

        if 'epsilon' in kwargs: self.epsilon = kwargs['epsilon']
        else: self.epsilon = 1

        if 'min_epsilon' in kwargs: self.min_epsilon = kwargs['min_epsilon']
        else: self.min_epsilon = 0.1

        if 'epsilon_decay' in kwargs: self.epsilon_decay = kwargs['epsilon_decay']
        else: self.epsilon_decay = 0.005

class Model():
    def __init__(num_observations, num_actions):
        pass


