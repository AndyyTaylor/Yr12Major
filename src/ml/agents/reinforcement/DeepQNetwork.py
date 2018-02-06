import numpy as np
import random

from .. import NN

class DeepQNetwork():
    def __init__(self, observation_space, action_space, gamma=0.9, epsilon=0.5, min_epsilon=0.1, epsilon_decay=0.95):
        self.action_space = action_space
        self.observation_space = observation_space

        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay


        input_nodes = self.observation_space.shape[0]
        output_nodes = self.action_space.n

        self.model = NN(input_nodes, 10, 4, 4, output_nodes, -1)

        self.memory = []
        self.batch_size = 200

    def reset(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def memorize(self, replay):
        # replay = (observations, new_observations, action, reward, done)
        self.memory.append(replay)

        if len(self.memory) > self.batch_size:
            self.memory.pop(0)

    def choose_action(self, observations):
        if random.random() > self.epsilon:
            action = self.model.predict(np.vstack((np.zeros((1, 2)), np.array(observations))))
        else:
            action = self.action_space.sample()

        return action

    def create_rewards(self, rewards):

        # new_rewards = new_rewards[::-1]
        rewards -= np.mean(rewards)
        # new_rewards /= np.std(new_rewards)

        return rewards

    def train(self, prev_obvs, new_obvs, action, reward, done):
        self.memorize((prev_obvs, new_obvs, action, reward, done))

        if not done or len(self.memory) < self.batch_size:
            return

        X = np.array([x[0] for x in self.memory])
        new_X = np.array([x[1] for x in self.memory])
        actions = np.array([x[2] for x in self.memory])
        rewards = np.array([x[3] for x in self.memory])
        dones = np.array([x[4] for x in self.memory])

        Q = self.model.feed_forward(X)
        Qn = self.model.feed_forward(new_X)

        rewards = self.create_rewards(rewards)

        y = np.zeros((len(self.memory), self.action_space.n))

        for i in range(len(self.memory)):
            y[i] = Q[i]

            y[i, actions[i]] = rewards[i]
            if not dones[i]:
                y[i, actions[i]] += self.gamma * np.max(Qn[i])
        print(y)
        self.model.train(X, y, 10)
        self.memory = []

    def play(self, observations, reward, done, training=True):

        return self.choose_action(observations)

