import numpy as np


def sigmoid(a):
    return 1 / (1 + np.exp(-a))


def softmax(a):
    expA = np.exp(a)
    return expA / expA.sum(axis=1, keepdims=True)


class Dense():
    def __init__(self, num_nodes, input_shape=None, function='sigmoid'):
        self.num_nodes = num_nodes
        self.input_shape = input_shape

        if function == 'sigmoid':
            self.func = sigmoid
        elif function == 'softmax':
            self.func = softmax
        else:
            raise NotImplementedError("Unknown function: " + function)

    def init(self):
        self.weights = np.random.randn(self.input_shape, self.num_nodes)
        self.bias = np.random.randn(self.num_nodes)

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape

    def _feed_forward(self, X):
        return self.func(X.dot(self.weights) + self.bias)
