import numpy as np


class NeuralNetwork():
    def __init__(self, environment):
        self.layers = []

        self.num_iters = 200

    def add_layer(self, layer):
        if self.layers:
            layer.set_input_shape(self.layers[-1].num_nodes)

        layer.init()
        self.layers.append(layer)

    def clear_layers(self):
        self.layers = []

    def predict(self, X):
        return np.argmax(self.feed_forward(X), axis=1)

    def feed_forward(self, X):
        for layer in self.layers:
            X = layer.feed_forward(X)

        return X

    def train(self, X, y, num_iters=1000):
        for i in range(self.num_iters):
            self.back_propagate(X, y)

    def back_propagate(self, X, y):
        P = self.feed_forward(X)

        t = np.zeros(P.shape)
        for m in range(len(y)):
            t[m, int(y[m])] = 1

        # cost = 0    # terribly implemented cross entropy cost function
        # for m in range(len(y)):
        #     for i in range(len(t[0])):
        #         cost += t[m, i] * np.log(max(P[m, i], 1e-120)) + (1 - t[m, i]) \
        #             * np.log(max(1 - P[m, i], 1e-120))

        grad = (1 / len(y)) * (t - P)   # normalized gradient

        for layer in reversed(self.layers):
            grad = layer.back_propagate(grad)
