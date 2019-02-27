import numpy as np
import random
from .config import *

class QLearn():
    def __init__(self, max_actions):
        self.Q = np.zeros((1, max_actions))
        self.state = 0
        self.prev_action = 0
        self.human_control = True
        self.moves = 0
        self.episodes = 1
        self.max_actions = max_actions

    def update(self, new_state, reward):
        while len(self.Q) < new_state:
            self.Q = np.vstack([self.Q, [0 for i in range(self.max_actions)]])
        self.Q[self.state][self.prev_action] += LEARNING_RATE * (reward + DISCOUNT_FACTOR * (self.maxQ(new_state)) - self.Q[self.state][self.prev_action])
        self.state = new_state

        self.moves+=1

    def reset(self, state):
        self.state = int(state)
        self.moves = 0
        self.episodes += 1

        while len(self.Q) < state+1:
            self.Q = np.vstack([self.Q, [0 for i in range(self.max_actions)]])

    def getAction(self):
        # alpha = max(EPSILON / self.episodes, 0.00)
        alpha = EPSILON
        if random.random() > alpha:
            indices = []
            max_val = self.Q[self.state].max()
            for i in range(len(self.Q[self.state])):
                if self.Q[self.state][i] == max_val:
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

