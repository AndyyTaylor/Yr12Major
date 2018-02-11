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
        return np.argmax(self.feed_forward(X))

    def train(self, prev_state, action, reward, done, new_state, alpha, gamma):
        out = self.feed_forward(prev_state)
        pred_out = self.feed_forward(new_state)

        y = out
        if done:
            y[0][action] += alpha * (reward - y[0][action])
        else:
            y[0][action] += alpha * (reward + gamma * np.max(pred_out) - y[0][action])

        self.back_prop(prev_state, y, alpha)

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

        D = np.subtract(self.feed_forward(X), y)

        for layer in reversed(self.layers):
            D = layer.back_prop(D, alpha, m)
