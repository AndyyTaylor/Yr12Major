import random
import numpy as np

from .agent import RLAgent
from .policies import *


class _DynamicProgramming(RLAgent):
    def __init__(self, num_observations, num_actions, alpha=0.5, gamma=0.9, policy='eps-greedy', **kwargs):
        self.num_actions = num_actions
        self.num_observations = num_observations

        self.alpha = alpha
        self.gamma = gamma

        self.policy = get_policy(policy)(num_observations, num_actions, **kwargs)

        self.V = {}

        self.state_id = -1
        self.state_ids = {}
        self.state_history = []

    def choose_action(self, state, env=None, **extras):
        if env is None:
            raise AttributeError("DP requires access to environment")

        return self.policy.choose_action(self.get_state_id(state), self._choose_action, env=env)

    def train(self, prev_state, action, reward, done, new_state, env=None):
        if env is None:
            raise AttributeError("DP requires access to environment")

        self._train(prev_state, action, reward, done, new_state, env)

        self.policy.update(prev_state, action, reward, done, new_state)

    def get_val(self, state, **extras):
        return self.V[self.get_state_id(state)]

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


class ValueFunction(_DynamicProgramming):
    def __init__(self, num_observations, num_actions, **kwargs):
        super().__init__(num_observations, num_actions, **kwargs)

    def _choose_action(self, state, env):
        best_action = 0

        for i in range(1, self.num_actions):  # Finds optimal action by looking at which action leads to which state
            new_state = self.get_state_id(env.get_state_if_move(i))
            best_state = self.get_state_id(env.get_state_if_move(best_action))

            if best_state == state or (new_state != state and self.V[new_state] > self.V[best_state]):
                best_action = i

        return best_action

    def _train(self, prev_state, action, reward, done, new_state, env):
        self.remember_state(prev_state)

        if done:
            self.remember_state(new_state)

            self.update(reward)

    def update(self, reward):
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])  # Updates old state values with learning rate
            self.V[prev] = value
            target = value * self.gamma  # Discounts state values using time

        self.clear_history()

    def remember_state(self, state):
        sid = self.get_state_id(state)
        self.state_history.append(sid)

    def clear_history(self):
        self.state_history = []


class _Iteration(_DynamicProgramming):
    def __init__(self, num_observations, num_actions, env=None, **kwargs):
        super().__init__(num_observations, num_actions, **kwargs)

        self.THRESHOLD = 1e-3

        self.converged = False
        self._policy = {}

        self.init_policy_and_v(env)  # Requires ability to loop through all possible states

        self.loop(env)

    def _choose_action(self, state, env):
        return self._policy[state]

    def _train(self, prev_state, action, reward, done, new_state, env):
        if done:
            self.loop(env, 1)

    def init_policy_and_v(self, env):
        for s in env.get_all_states():
            sid = self.get_state_id(s)

            if not env.is_terminal(s):
                self.V[sid] = np.random.random()
                self._policy[sid] = env.sample_action()

    def policy_improvement(self, env):  # Improves policy based off value function
        is_converged = True

        for s in env.get_all_states():
            sid = self.get_state_id(s)

            if sid in self._policy:
                old_a = self._policy[sid]  # a = action
                new_a = None
                best_val = float('-inf')

                for a in range(self.num_actions):
                    env.set_state(s)
                    obvs, reward, done, _ = env.step(a)  # hypothetically go through each action
                    v = reward + self.gamma * self.V[self.get_state_id(obvs)]  # Calculate expected return

                    if v > best_val:
                        best_val = v
                        new_a = a

                self._policy[sid] = new_a  # Update policy
                if new_a != old_a:
                    is_converged = False

        return is_converged


class PolicyIteration(_Iteration):

    def loop(self, env, max_iters=None):
        iters = 0
        while not self.converged and (max_iters is None or iters < max_iters):
            self.policy_evaluation(env)  # Update value function given current policy (prediction problem)
            self.converged = self.policy_improvement(env)  # Improve policy given new value function (control problem)
            iters += 1

    def policy_evaluation(self, env):
        while True:
            biggest_change = 0
            for s in env.get_all_states():
                sid = self.get_state_id(s)

                old_v = self.V[sid]

                if sid in self._policy:
                    a = self._policy[sid]
                    env.set_state(s)

                    obvs, reward, done, _ = env.step(a)
                    self.V[sid] = reward + self.gamma * self.V[self.get_state_id(obvs)]  # Expected return given policy (E[G(t) | policy])

                    biggest_change = max(biggest_change, np.abs(old_v - self.V[sid]))

            if biggest_change < self.THRESHOLD:
                break


class ValueIteration(_Iteration):

    def loop(self, env, max_iters=None):
        num_iters = 0
        while not self.converged and (max_iters is None or num_iters < max_iters):
            self.converged = self.value_iteration(env)  # Improve values, by looping through all actions rather than using policy (prediction)
            num_iters += 1

        self.policy_improvement(env)  # Using converged values, update policy (control)

    def value_iteration(self, env):
        biggest_change = 0

        for state in env.get_all_states():
            sid = self.get_state_id(state)

            old_v = self.V[sid]

            if sid in self._policy:
                new_v = float('-inf')
                for a in range(self.num_actions):
                    env.set_state(state)
                    obvs, reward, done, _ = env.step(a)

                    v = reward + self.gamma * self.V[self.get_state_id(obvs)]

                    if v > new_v:
                        new_v = v

                self.V[sid] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - new_v))

        return biggest_change < self.THRESHOLD
