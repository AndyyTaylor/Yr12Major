import random
import numpy as np

class QLearn():
    def __init__(self, num_observations, num_actions, alpha=0.02, gamma=0.95, epsilon=1, min_epsilon=0.05, epsilon_decay=0.0001):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay

        self.num_actions = num_actions
        self.num_observations = num_observations

        self.model = SarsaTabular(num_observations, num_actions, self.alpha, self.gamma)

    def choose_action(self, state):
        if random.random() > self.epsilon:
            return self.model.get_optimal_action(state)

        return random.randint(0, self.num_actions-1)

    def reset(self):
        self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)

    def train(self, prev_state, action, reward, done, new_state):
        self.model.set_epsilon(self.epsilon)
        self.model.train(prev_state, action, reward, done, new_state)

class Model():
    def __init__(self, num_observations, num_actions, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.num_observations = num_observations

    def get_optimal_action(self, state):
        return random.randint(0, self.num_actions-1)

    def train(self, prev_state, action, reward, done, new_state):
        print("Train not implemented")

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


    def get_optimal_action(self, state):
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
                self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * np.max(self.Q[new_sid]))
            else:
                self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * self.Q[new_sid][random.randint(0, self.num_actions-1)])

