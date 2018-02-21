import random, sys, time
import numpy as np
import copy

from ..deeplearning.nn import NeuralNetwork
from ..deeplearning.layers import Dense
from ..deeplearning.loss_functions import SquareLoss

class QLearn():
    def __init__(self, num_observations, num_actions, alpha=0.01, gamma=0.99, epsilon=1, min_epsilon=0.01, epsilon_decay=0.005):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay

        self.num_actions = num_actions
        self.num_observations = num_observations

        # self.model = Tabular(num_observations, num_actions, self.alpha, self.gamma)
        self.isnn = True
        self.model = NeuralNetwork(SquareLoss)
        self.model.add_layer(Dense(256, 'relu', input_shape=num_observations))
        self.model.add_layer(Dense(512, 'relu'))
        self.model.add_layer(Dense(num_actions, 'linear'))

        self.old_model = copy.deepcopy(self.model)

        self.MAX_MEMORY = 500000
        self.batch_size = 32

        self.memory = []

        self.new_util = 0
        self.step = 0

    def choose_action(self, state, epsilon=-1):
        if epsilon == -1: epsilon = self.epsilon

        if random.random() > self.epsilon:
            return int(self.model.predict(np.array(state)))

        return random.randint(0, self.num_actions-1)

    def reset(self):
        print(self.model.feed_forward(np.array([1, 0, 0, 0])))
        print(self.model.predict(np.array([1, 0, 0, 0])))
        # print(self.model.predict(np.array([0.3, 1])), self.model.predict(np.array([1, 1])), self.model.predict(np.array([1, 0.3])))
        self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)

    def train(self, prev_state, action, reward, done, new_state):

        if self.isnn:
            self.memorize(prev_state, action, reward, done, new_state)
            # print(reward)

            samples = np.random.choice(len(self.memory), min(len(self.memory), self.batch_size))
            for idx in samples:
                replay = self.memory[idx]
                state, action, reward, done, new_state = replay

                new_utility = self.old_model.feed_forward(new_state)[0]
                if np.random.random() < 0.1: self.new_util = new_utility

                y = self.model.feed_forward(state)[0]

                if done:
                    y[action] += self.alpha * (reward - y[action])
                else:
                    y[action] += self.alpha * (reward + self.gamma * np.max(new_utility) - y[action])

                self.model.train(np.array([state]), np.array([y]), 1, 1)

                self.step += 1

                if self.step % 1000 == 0:
                    self.old_model = copy.deepcopy(self.model)
                    print("Update model")

            # print(new_util)
        else:
            self.model.train(prev_state, action, reward, done, new_state)

    def memorize(self, prev_state, action, reward, done, new_state):
        self.memory.append(np.array([prev_state, action, reward, done, new_state]))

        if len(self.memory) > self.MAX_MEMORY:
            self.memory.pop(0)

class Model():
    def __init__(self, num_observations, num_actions, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.num_observations = num_observations

    def predict(self, state):
        return random.randint(0, self.num_actions-1)

    def train(self, prev_state, action, reward, done, new_state):
        print("Train not implemented")

    def set_epsilon(self, e):
        pass

class Tabular(Model):
    def __init__(self, num_observations, num_actions, alpha, gamma):
        super().__init__(num_observations, num_actions, alpha, gamma)

        self.Q = np.zeros((1, self.num_actions))

        self.state_ids = {}
        self.state_id = -1

    def train(self, prev_state, action, reward, done, new_state):
        prev_sid = self.get_state_id(prev_state)
        new_sid = self.get_state_id(new_state)

        if done:
            self.Q[prev_sid][action] += self.alpha * (reward - self.Q[prev_sid][action])
        else:
            self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * np.max(self.Q[new_sid]) - self.Q[prev_sid][action])

    def predict(self, state):
        sid = self.get_state_id(state)

        return np.argmax(self.Q[sid])

    def get_state_id(self, state):
        str_state = str(state)

        if str_state not in self.state_ids:
            self.state_ids[str_state] = self.gen_state_id()

        return self.state_ids[str_state]

    def gen_state_id(self):
        self.state_id += 1
        self.Q = np.vstack([self.Q, [0 for i in range(self.num_actions)]])

        return self.state_id
    #
    # def predict(self, state):
    #     return self.Q[self.get_state_id(state)]

class SarsaTabular(Tabular):
    def set_epsilon(self, e):
        self.epsilon = e

    def train(self, prev_state, action, reward, done, new_state):
        prev_sid = self.get_state_id(prev_state)
        new_sid = self.get_state_id(new_state)

        if done:
            self.Q[prev_sid][action] = self.alpha * reward
        else:
            if random.random() > self.epsilon:
                self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * np.max(self.Q[new_sid]) - self.Q[prev_sid][action])
            else:
                self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * self.Q[new_sid][random.randint(0, self.num_actions-1)] - self.Q[prev_sid][action])

