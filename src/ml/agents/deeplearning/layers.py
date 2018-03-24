import numpy as np
from .functions import *


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

        if X.ndim == 3:
            out = np.zeros((X.shape[0], X.shape[1], self.num_nodes))
            for t in range(X.shape[1]):
                out[:, t, :] = X[:, t, :].dot(self.weights) + self.bias
            return out
        else:
            return X.dot(self.weights) + self.bias

    def back_propagate(self, grad, learning_rate=0.01):
        weights = self.weights
        print(weights.max())

        if grad.ndim == 3:
            new_grad = np.zeros((grad.shape[0], grad.shape[1], self.input_shape))
            for t in range(grad.shape[1]):
                self.weights += learning_rate * self.input_layer[:, t, :].T.dot(grad[:, t, :])
                # self.bias += learning_rate * np.sum(grad[:, t, :], axis=0)
                new_grad[:, t, :] = grad[:, t, :].dot(weights.T)
            return new_grad
        else:
            self.weights += learning_rate * self.input_layer.T.dot(grad)
            self.bias += learning_rate * np.sum(grad, axis=0)

            return grad.dot(weights.T)


class Activation():
    def __init__(self, function):
        self.func = get_function(function)()

    def init(self):
        pass

    def set_input_shape(self, num_nodes):
        self.num_nodes = num_nodes

    def feed_forward(self, X):
        self.input_layer = X

        if X.ndim == 3:
            out = np.zeros_like(X)
            for t in range(X.shape[1]):
                out[:, t, :] = self.func(X[:, t, :])
            return out
        else:
            return self.func(X)

    def back_propagate(self, grad, _):
        if grad.ndim == 3:
            out = np.zeros_like(grad)
            for t in range(grad.shape[1]):
                out[:, t, :] = self.func(grad[:, t, :])
            return out
        else:
            return grad * self.func.grad(self.input_layer, True)


class Recurrent():
    def __init__(self, num_nodes, input_shape=None, bbtt_trunc=8):
        self.num_nodes = num_nodes
        self.input_shape = input_shape

        self.past_states = []
        self.all_past_states = []

    def init(self):
        self.x_weights = np.random.random((self.input_shape, self.num_nodes)) * 2 - 1
        self.h_weights = np.random.random((self.num_nodes, self.num_nodes)) * 2 - 1

        self.bias = np.random.randn(self.num_nodes) * 2 - 1  # I think I only need 1 of these

    def feed_forward(self, X):
        self.o = []
        self.reset_past_states(len(X))

        for t in range(len(X)):
            ret = X[t, :].dot(self.x_weights) + self.past_states[t-1].dot(self.h_weights)  # + self.bias
            self.past_states[t] = ret
            self.o.append(ret)

        return np.array(self.o)

    def back_propagate(self, grad):

        grad_x_weights = np.zeros_like(self.x_weights)
        grad_h_weights = np.zeros_like(self.h_weights)

        grad_grad = np.zeros_like(grad)

        for t in reversed(range(len(self.past_states))):
            print(t)

        return grad

    def reset_past_states(self, t):
        self.all_past_states += self.past_states
        self.past_states = [0 for x in range(t-1)] + [np.zeros(self.num_nodes)]

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape
