import numpy as np
from .functions import *


class Recurrent():
    def __init__(self, num_nodes, input_shape=None):
        self.num_nodes = num_nodes
        self.input_shape = input_shape

        self.bptt_trunc = 4

    def init(self):  # V is handled by the next layer
        self.U = 0.1 * np.random.random((self.input_shape, self.num_nodes)) - 0.05
        self.W = 0.1 * np.random.random((self.num_nodes, self.num_nodes)) - 0.05
        self.V = 0.1 * np.random.random((self.num_nodes, self.num_nodes)) - 0.05

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape

    def feed_forward(self, X):
        assert X.ndim == 3

        T = X.shape[1]

        self.layer_input = X

        self.states = np.zeros((X.shape[0], T + 1, self.num_nodes))
        self.states[:, -1] = np.zeros((X.shape[0], self.num_nodes))

        self.out = np.zeros((X.shape[0], T, self.num_nodes))

        for t in range(T):
            self.states[:, t] = X[:, t, :].dot(self.U) + self.states[:, t-1].dot(self.W)
            self.out[:, t] = self.states[:, t].dot(self.V)
            # print(self.states[:, t])

        return self.out  # Don't send initial hidden

    def back_propagate(self, grad):
        T = grad.shape[1]

        grad_U = np.zeros_like(self.U)
        grad_W = np.zeros_like(self.W)
        grad_V = np.zeros_like(self.V)

        new_grad = np.zeros((grad.shape[0], grad.shape[1], self.input_shape))

        for t in reversed(range(T)):
            grad_V += grad[:, t, :].T.dot(self.states[:, t])

            grad_state = grad[:, t, :].dot(self.V)

            new_grad[:, t, :] = grad_state.dot(self.U.T)

            for bt in reversed(range(max(0, t-self.bptt_trunc), t+1)):  # from the current time step to t=0 or bbt_trunc time steps
                grad_U += self.layer_input[:, bt, :].T.dot(grad_state)
                grad_W += self.states[:, bt-1].T.dot(grad_state)

                grad_state = grad_state.dot(self.W)  # wrt to W as that's the matrix that gets multiplied to state inputs

        self.U += 0.3 * grad_U
        self.V += 0.3 * grad_V
        self.W += 0.3 * grad_W

        return new_grad


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
        self.input_layer = X

        if X.ndim == 3:
            out = np.zeros_like(X)
            for t in range(X.shape[1]):
                out[:, t, :] = self.func(X[:, t, :])
            return out
        else:
            return self.func(X)

    def back_propagate(self, grad):
        if grad.ndim == 3:
            out = np.zeros_like(grad)
            for t in range(grad.shape[1]):
                out[:, t, :] = grad[:, t, :] * self.func.grad(self.input_layer[:, t, :], True)
            return out
        else:
            return grad * self.func.grad(self.input_layer, True)
