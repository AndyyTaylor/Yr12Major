import random
import numpy as np

class NeuralNetwork():

    def __init__(self, loss):
        self.loss_function = loss()

        self.layers = []

    def add_layer(self, layer):
        if self.layers:     # by default, containers equate len(container) > 0
            layer.set_input_shape(self.layers[-1].num_nodes)

        if layer.requires_init:
            layer.initialize()

        self.layers.append(layer)

    def predict(self, X):
        if len(X.shape) < 2:
            X = X.reshape(1, 784)
        output = self.feed_forward(X)

        if len(output.shape) > 1:
            return np.argmax(output, axis=1)

        return np.argmax(output)

    def train(self, X, y, num_iters):
        for i in range(num_iters):
            out = self.feed_forward(X)
            self.back_prop(X, y, 0.001)
            new_out = self.feed_forward(X)
            # print(out)
            # print(new_out)
            print(self.cost(X, y))

    def train_rl(self, prev_state, action, reward, done, new_state, alpha, gamma):
        out = self.feed_forward(prev_state)
        pred_out = self.feed_forward(new_state)

        y = out
        if done:
            y[0][action] += alpha * (reward - y[0][action])
        else:
            y[0][action] += alpha * (reward + gamma * np.max(pred_out) - y[0][action])

        print('------------')
        print(self.cost(prev_state, y))
        for i in range(10): self.back_prop(prev_state, y, alpha)
        print(self.cost(prev_state, y))

    def feed_forward(self, X):
        if len(X.shape) < 2:
            X = X.reshape((1, X.shape[0]))

        for layer in self.layers:
            X = layer.feed_forward(X)
        return X

    def back_prop(self, X, y, alpha):
        m = len(y)
        if len(X.shape) < 2:
            X = X.reshape((1, X.shape[0]))

        for i in range(m):
            o = self.feed_forward(X[i])

            lbl = np.zeros((10, 1))
            lbl[int(y[i]), 0] = 1
            delta = np.subtract(o[0], lbl.T).T

            for layer in reversed(self.layers):
                delta = layer.back_prop(delta, alpha, m)

    def cost(self, X, y):
        lbl = np.zeros((len(y), 10))
        for i in range(len(y)):
            lbl[i, int(y[i])] = 1
        print(lbl)
        o = self.feed_forward(X)
        return (1.0/2) * np.sum(np.subtract(o, lbl) ** 2)
