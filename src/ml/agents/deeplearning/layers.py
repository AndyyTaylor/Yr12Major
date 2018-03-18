import numpy as np


def sigmoid(a):
    return 1 / (1 + np.exp(-a))


def sig_grad(a):
    return a * (1 - a)


def softmax(a):
    expA = np.exp(a)
    return expA / expA.sum(axis=1, keepdims=True)


class Dense():
    def __init__(self, num_nodes, input_shape=None):
        self.num_nodes = num_nodes
        self.input_shape = input_shape

    def init(self):
        self.weights = 2 * np.random.random((self.input_shape, self.num_nodes)) - 1
        self.bias = 2 * np.random.random(self.num_nodes) - 1

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape

    def feed_forward(self, X):
        self.input_layer = X

        return X.dot(self.weights) + self.bias

    def back_propagate(self, grad):
        weights = self.weights

        self.weights += 0.0001 * self.input_layer.T.dot(grad)
        self.bias += 0.0001 * np.sum(grad, axis=0)

        return grad.dot(weights.T)


class Activation():
    def __init__(self, function):
        self.func_grad = sig_grad
        if function == 'sigmoid':
            self.func = sigmoid
        elif function == 'softmax':
            self.func = softmax
        else:
            raise NotImplementedError("Function not found:", function)

    def init(self):
        pass

    def set_input_shape(self, num_nodes):
        self.num_nodes = num_nodes

    def feed_forward(self, X):
        self.input_layer = self.func(X)

        return self.input_layer

    def back_propagate(self, grad):
        return grad * self.func_grad(self.input_layer)
