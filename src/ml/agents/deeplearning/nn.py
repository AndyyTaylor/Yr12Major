import numpy as np


def softmax(a):
    expA = np.exp(a)
    return expA / expA.sum(axis=1, keepdims=True)


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

        t = np.zeros(P.shape)
        for m in range(len(y)):
            t[m, y[m]] = 1

        cost = 0
        for m in range(len(y)):
            for i in range(len(t[0])):
                cost += t[m, i] * np.log(max(P[m, i], 1e-120)) + (1 - t[m, i]) * np.log(max(1 - P[m, i], 1e-120))

        grad = (t - P)

        for layer in reversed(self.layers):
            grad = layer.back_propagate(grad)

        print(cost)
