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
        if X.ndim == 3:
            return np.argmax(self.feed_forward(X), axis=2)
        else:
            return np.argmax(self.feed_forward(X), axis=1)

    def feed_forward(self, X):
        for layer in self.layers:
            X = layer.feed_forward(X)

        return X

    def back_propagate(self, X, y):
        P = self.feed_forward(X)

        grad = -(1 / y.shape[0]) * (y - P)   # normalized gradient
        print('gmax', grad.max())
        for layer in reversed(self.layers):
            grad = layer.back_propagate(grad, 0.00001)

        input()

        print(P[0])
        print(y[0])
