import numpy as np

import numpy as np
import random
from .config import *

class OldQLearn():
    def __init__(self, num_actions):
        self.Q = np.zeros((1, num_actions))
        self.state = 0
        self.prev_action = 0
        self.human_control = True
        self.moves = 0
        self.episodes = 1
        self.max_actions = num_actions
        self.alpha = EPSILON
        self.all_states = {}
        self.state_id = 0

    def update(self, new_state, reward, done):
        while len(self.Q) < self.get_state_id(new_state):
            self.Q = np.vstack([self.Q, [0 for i in range(self.max_actions)]])
        if not done:
            self.Q[self.state][self.prev_action] += LEARNING_RATE * (reward + DISCOUNT_FACTOR * (self.maxQ(self.get_state_id(new_state))) - self.Q[self.state][self.prev_action])
        else:
            self.Q[self.state][self.prev_action] += LEARNING_RATE * reward
        self.state = self.get_state_id(new_state)

        self.moves+=1

    def get_state_id(self, state):
        state = str(state)

        if not state in self.all_states:
            self.all_states[state] = self.state_id
            self.state_id += 1

        return self.all_states[state]

    def reset(self, state):
        self.state = self.get_state_id(state)
        self.moves = 0
        self.episodes += 1
        self.alpha = max(EPS_MIN, self.alpha * EPS_DECAY)

        while len(self.Q) < self.state+1:
            self.Q = np.vstack([self.Q, [0 for i in range(self.max_actions)]])

    def get_action(self, state):
        # alpha = max(EPSILON / self.episodes, 0.00)
        state = self.get_state_id(state)

        while len(self.Q) < state+1:
            self.Q = np.vstack([self.Q, [0 for i in range(self.max_actions)]])

        if random.random() > self.alpha:
            indices = []
            max_val = self.Q[state].max()
            for i in range(len(self.Q[state])):
                if self.Q[state][i] == max_val:
                    indices.append(i)

            act = random.choice(indices)
        else:
            act = random.randint(0, self.max_actions-1)
        self.prev_action = act
        return act

    def maxQ(self, state):
        while len(self.Q) < state+1:
            self.Q = np.vstack([self.Q, [0 for i in range(self.max_actions)]])
        return self.Q[state].max()

