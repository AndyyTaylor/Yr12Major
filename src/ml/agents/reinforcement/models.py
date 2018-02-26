import random
import numpy as np


class Model():
    def __init__(self, num_observations, num_actions, alpha=0.01, gamma=0.99):
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.num_observations = num_observations

    def predict(self, state, **extras):
        return random.randint(0, self.num_actions-1)

    def train(self, prev_state, action, reward, done, new_state):
        print("Train not implemented")

    def set_epsilon(self, e):
        pass


class ValueIteration(Model):
    def __init__(self, num_observations, num_actions, **extras):
        super().__init__(num_observations, num_actions)

        self.state_id = -1
        self.V = {}
        self.state_ids = {}
        self.state_history = []

    def predict(self, state, env=0, **extras):
        best_action = 0

        for i in range(1, self.num_actions):
            new_state = self.get_state_id(env.get_state_if_move(i, 1))
            best_state = self.get_state_id(env.get_state_if_move(best_action, 1))

            if best_state == self.get_state_id(state) or (new_state != self.get_state_id(state) and self.V[new_state] > self.V[best_state]):
                best_action = i

        return best_action

    def train(self, prev_state, action, reward, done, new_state):
        self.remember_state(prev_state)

        if done:
            pass

    def remember_state(self, state):
        sid = self.get_state_id(state)
        self.state_history.append(sid)

    def get_state_id(self, state):
        str_state = str(state)

        if str_state not in self.state_ids:
            self.state_ids[str_state] = self.gen_state_id()

        if self.state_ids[str_state] not in self.V:
            self.V[self.state_ids[str_state]] = 0

        return self.state_ids[str_state]

    def gen_state_id(self):
        self.state_id += 1

        return self.state_id


class Tabular(Model):
    def __init__(self, num_observations, num_actions, alpha=0.01, gamma=0.99, **extras):
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

    def predict(self, state, **extras):
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
            self.Q[prev_sid][action] += self.alpha * (reward - self.Q[prev_sid][action])
        else:
            if random.random() > self.epsilon:
                self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * np.max(self.Q[new_sid]) - self.Q[prev_sid][action])
            else:
                self.Q[prev_sid][action] += self.alpha * (reward + self.gamma * self.Q[new_sid][random.randint(0, self.num_actions-1)] - self.Q[prev_sid][action])
