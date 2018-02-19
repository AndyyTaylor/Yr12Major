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
            X = X.reshape(1, X.shape[0])
        output = self.feed_forward(X)

        if len(output.shape) > 1:
            return np.argmax(output, axis=1)

        return np.argmax(output)

    def train(self, X, y, num_iters, alpha=0.01):
        for i in range(num_iters):
            out = self.feed_forward(X)
            self.back_prop(X, y, alpha)

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

            delta = np.subtract(o[0], y[i].reshape(1, y.shape[1])).T

            for layer in reversed(self.layers):
                delta = layer.back_prop(delta, alpha, m)

    def cost(self, X, y):
        # print(lbl)
        o = self.feed_forward(X)
        return (1.0/2) * np.sum(np.subtract(o, y) ** 2)
