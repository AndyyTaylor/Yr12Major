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

        return X.dot(self.weights) + self.bias

    def back_propagate(self, grad):
        weights = self.weights

        self.weights += 0.1 * self.input_layer.T.dot(grad)
        self.bias += 0.1 * np.sum(grad, axis=0)

        return grad.dot(weights.T)


class Activation():
    def __init__(self, function):
        self.func = get_function(function)()

    def init(self):
        pass

    def set_input_shape(self, num_nodes):
        self.num_nodes = num_nodes

    def feed_forward(self, X):
        self.input_layer = self.func(X)

        return self.input_layer

    def back_propagate(self, grad):
        return grad * self.func.grad(self.input_layer)


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
        self.reset_time = 9
        self.o = []

        for time in range(len(X)):
            t = time % self.reset_time
            if t == 0:
                self.reset_past_states()

            ret = X[t].dot(self.x_weights) + self.bias + self.past_states[-1].dot(self.h_weights)
            self.past_states.append(ret)
            self.o.append(ret)

        print(len(self.all_past_states))
        return np.array(self.o)

    def back_propagate(self, grad):
        return grad

    def reset_past_states(self):
        self.all_past_states += self.past_states
        self.past_states = [np.zeros(self.num_nodes)]

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape
