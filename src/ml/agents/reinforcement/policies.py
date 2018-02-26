import random
import numpy as np


class Policy():
    def __init__(self, num_observations, num_actions, **extras):
        self.num_actions = num_actions
        self.num_observations = num_observations

    def choose_action(self, state, optimal_action, **kwargs):
        if random.random() > self.epsilon:
            return optimal_action(state, **kwargs)

        return random.randint(0, self.num_actions-1)

    def update(self, prev_state, action, reward, done, new_state):
        return


class Greedy(Policy):
    def choose_action(self, state, optimal_action, **kwargs):
        return optimal_action(state, **kwargs)


class EpsGreedy(Policy):
    def __init__(self, num_observations, num_actions, epsilon=1, min_epsilon=0.1, epsilon_decay=0.001, **extras):
        super().__init__(num_observations, num_actions)

        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay

    def choose_action(self, state, optimal_action, **kwargs):
        if random.random() > self.epsilon:
            return optimal_action(state, **kwargs)

        return random.randint(0, self.num_actions-1)

    def update(self, prev_state, action, reward, done, new_state):

        if done:
            self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)
