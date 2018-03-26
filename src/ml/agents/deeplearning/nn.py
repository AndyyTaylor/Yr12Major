import numpy as np


class NeuralNetwork():
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        if self.layers:
            layer.set_input_shape(self.layers[-1].num_nodes)

        layer.init()
        self.layers.append(layer)

    def predict(self, X):
        return np.argmax(self.feed_forward(X), axis=1)

    def feed_forward(self, X):
        for layer in self.layers:
            X = layer.feed_forward(X)

        return X

    def back_propagate(self, X, y):
        P = self.feed_forward(X)
        # print(P[0, 4])

        cost = 0    # terribly implemented cross entropy cost function
        for m in range(len(y)):
            for t in range(y.shape[1]):
                for i in range(y.shape[2]):
                    cost += y[m, t, i] * np.log(max(P[m, t, i], 1e-12))

        print(cost)
        grad = (1 / len(y)) * (y - P)   # normalized gradient

        for layer in reversed(self.layers):
            grad = layer.back_propagate(grad)
