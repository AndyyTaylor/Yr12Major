import random
import numpy as np
from math import e, log

class Layer():
    def __init__(self, requires_init=False):
        self.requires_init = requires_init

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape

    def feed_forward(self, X):
        raise NotImplementedError()

class Dense(Layer):
    def __init__(self, num_nodes, activation, input_shape=None):
        super().__init__(True)

        self.num_nodes = num_nodes
        self.input_shape = input_shape
        self.A = None
        self.Z = None

        if activation == 'relu':
            self.func = self.relu
            self.func_grad = self.relu_grad
        else:
            self.func = self.linear
            self.func_grad = self.linear_grad

    def initialize(self):
        self.weights = self.init_weights(self.input_shape, self.num_nodes)

    def feed_forward(self, X):
        self.A = X
        X = np.insert(X, 0, 1, axis=1)
        self.A2 = X
        Z = X.dot(self.weights.T)
        self.Z = self.func(Z)

        return self.func(Z)

    def back_prop(self, delta, alpha, m):
        W = np.copy(self.weights)

        if np.any(np.isnan(delta)):
            print(self.weights.shape)
        # print((1.0 / m) * alpha * self.A2.T.dot(delta.T).T)
        self.weights -= (1.0 / m) * alpha * self.A2.T.dot(delta.T).T

        delta = np.multiply(W.T.dot(delta)[1:], self.func_grad(self.A.T))

        return delta

    def init_weights(self, in_layer, out_layer):
        epsilon_init = 0.12
        W = np.random.rand(out_layer, in_layer + 1) * 2 * epsilon_init - epsilon_init

        return W

    def linear(self, x):
        return x

    def linear_grad(self, x):
        return np.ones(x.shape)

    def relu(self, x):
        x[x<0] = 0
        return x

    def relu_grad(self, x):
        return (x > 0) * 1

    def tanh(self, x):
        return np.tanh(x)

    def tanh_grad(self, x):
        return (1 - (x ** 2))

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def g_prime(self, a):
        return np.multiply(a, np.subtract(1.0, a))

    def sig_grad(self, z):
        return np.multiply(self.sigmoid(z), (1 - self.sigmoid(z)))
