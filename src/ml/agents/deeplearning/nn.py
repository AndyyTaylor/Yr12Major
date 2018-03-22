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

        # t = np.zeros(P.shape)
        # for m in range(len(y)):
        #     t[m, int(y[m])] = 1

        cost = 0    # terribly implemented cross entropy cost function
        for m in range(len(y)):
            for i in range(len(y[0])):
                max(P[m, i], 1e-120)
                cost += y[m, i] * np.log(max(P[m, i], 1e-120)) + (1 - y[m, i]) * np.log(max(1 - P[m, i], 1e-120))
        # print(P[0].shape)
        # print(y[0])
        # print(X.shape)
        # print(y.shape)
        # print(P.shape)
        grad = (1 / len(y)) * (y.reshape(X.shape[0], X.shape[1], 1) - P)   # normalized gradient
        # print(grad.shape)
        for layer in reversed(self.layers):
            grad = layer.back_propagate(grad)

        print(cost)
