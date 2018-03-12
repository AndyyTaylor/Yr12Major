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
            X = layer._feed_forward(X)

        return X
