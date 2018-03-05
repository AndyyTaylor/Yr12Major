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
        pass

    def set_epsilon(self, e):
        pass


class StateValues(Model):
    def __init__(self, num_observations, num_actions, alpha=0.5, gamma=0.9, **extras):
        super().__init__(num_observations, num_actions)

        self.alpha = alpha

        self.state_id = -1
        self.V = {}
        self.state_ids = {}
        self.state_history = []

    def predict(self, state, env=0, **extras):
        best_action = 0

        for i in range(1, self.num_actions):
            new_state = self.get_state_id(env.get_state_if_move(i))
            best_state = self.get_state_id(env.get_state_if_move(best_action))

            if best_state == self.get_state_id(state) or (new_state != self.get_state_id(state) and self.V[new_state] > self.V[best_state]):
                best_action = i

        best_state = self.get_state_id(env.get_state_if_move(best_action))

        return best_action

    def get_val(self, state, env=0, **extras):
        sid = self.get_state_id(state)
        return self.V[sid]

    def train(self, prev_state, action, reward, done, new_state):
        self.remember_state(prev_state)

        if done:
            self.remember_state(new_state)

            self.update(reward)

    def update(self, reward):
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])
            self.V[prev] = value
            target = value * self.gamma
        self.clear_history()

    def remember_state(self, state):
        sid = self.get_state_id(state)
        self.state_history.append(sid)

    def clear_history(self):
        self.state_history = []

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


class PolicyIteration(Model):
    def __init__(self, num_observations, num_actions, gamma=0.99, env=None, **extras):
        super().__init__(num_observations, num_actions, gamma=0.99)

        self.THRESHOLD = 1e-3

        self.converged = False
        self.state_id = -1
        self.V = {}
        self.policy = {}
        self.state_ids = {}
        self.state_history = []

        self.initV(env)
        self.init_policy(env)

        self.policy_iter(env)

    def predict(self, state, **extras):
        return self.policy[self.get_state_id(state)]

    def get_val(self, state, **extras):
        sid = self.get_state_id(state)
        return self.V[sid]

    def policy_iter(self, env):
        while not self.converged:
            self.policy_evaluation(env)
            self.converged = self.policy_improvement(env)

    def policy_evaluation(self, env):
        while True:
            biggest_change = 0
            for s in env.get_all_states():
                sid = self.get_state_id(s)

                old_v = self.V[sid]

                if sid in self.policy:
                    a = self.policy[sid]
                    env.set_state(s)

                    obvs, reward, done, _ = env.step(a)
                    self.V[sid] = reward + self.gamma * self.V[self.get_state_id(obvs)]

                    biggest_change = max(biggest_change, np.abs(old_v - self.V[sid]))

            if biggest_change < self.THRESHOLD:
                break

    def policy_improvement(self, env):
        is_converged = True

        for s in env.get_all_states():
            sid = self.get_state_id(s)

            if sid in self.policy:
                old_a = self.policy[sid]
                new_a = None
                best_val = float('-inf')

                for a in range(self.num_actions):
                    env.set_state(s)
                    obvs, reward, done, _ = env.step(a)
                    v = reward + self.gamma * self.V[self.get_state_id(obvs)]

                    if v > best_val:
                        best_val = v
                        new_a = a

                self.policy[sid] = new_a
                if new_a != old_a:
                    is_converged = False

        return is_converged

    def initV(self, env):
        for s in env.get_all_states():
            sid = self.get_state_id(s)

            if not env.is_terminal(s):
                self.V[sid] = np.random.random()

    def init_policy(self, env):
        for s in env.get_all_states():
            sid = self.get_state_id(s)

            if not env.is_terminal(s):
                self.policy[sid] = env.sample_action()

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

    def get_val(self, state, action=None):
        sid = self.get_state_id(state)

        if action is None:
            action = self.predict(state)

        return self.Q[sid, action]

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
