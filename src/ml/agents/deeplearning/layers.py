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
    def __init__(self, num_nodes, input_shape=None):
        super().__init__(True)

        self.num_nodes = num_nodes
        self.input_shape = input_shape
        self.A = None
        self.Z = None

    def initialize(self):
        self.weights = self.init_weights(self.input_shape, self.num_nodes)

    def feed_forward(self, X):
        self.A = X
        X = np.insert(X, 0, 1, axis=1)
        Z = X.dot(self.weights.T)
        self.Z = Z

        return self.sigmoid(Z)

    def back_prop(self, D, alpha, m):
        print('back')
        print((self.weights.T.dot(D.T)[1:]).shape)
        D = np.multiply(self.weights.T.dot(D.T)[1:], self.sig_grad(self.Z.T))
        grad = D.dot(self.A)

        self.weights -= alpha * (1.0 / m) * grad

        return D

    def init_weights(self, in_layer, out_layer):
        epsilon_init = 0.12
        W = np.random.rand(out_layer, in_layer + 1) * 2 * epsilon_init - epsilon_init

        return W

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def sig_grad(self, z):
        return np.multiply(self.sigmoid(z), (1 - self.sigmoid(z)))
