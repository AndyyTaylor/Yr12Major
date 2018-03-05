import random
import numpy as np

from .models import *
from .policies import *


class QLearn():
    def __init__(self, num_observations, num_actions, model='tabular', policy='eps-greedy', **kwargs):
        self.num_actions = num_actions
        self.num_observations = num_observations

        if model == 'tabular':
            self.model = Tabular(num_observations, num_actions, **kwargs)
        elif model == 'state-values':
            self.model = StateValues(num_observations, num_actions, **kwargs)
        elif model == 'policy-iteration':
            self.model = PolicyIteration(num_observations, num_actions, **kwargs)
        else:
            raise NotImplementedError("Unknown Model: " + model)

        if policy == 'eps-greedy':
            self.policy = EpsGreedy(num_observations, num_actions, **kwargs)
        elif policy == 'greedy':
            self.policy = Greedy(num_observations, num_actions, **kwargs)
        else:
            raise NotImplementedError("Unknown Policy: " + policy)

    def choose_action(self, state, **kwargs):
        return self.policy.choose_action(state, self.optimal_action, **kwargs)

    def optimal_action(self, state, **kwargs):
        return int(self.model.predict(np.array(state), **kwargs))

    def train(self, prev_state, action, reward, done, new_state):
        self.model.train(prev_state, action, reward, done, new_state)
        self.policy.update(prev_state, action, reward, done, new_state)
