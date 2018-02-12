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
        # print(self.weights.shape)

    def feed_forward(self, X):
        self.A = X
        X = np.insert(X, 0, 1, axis=1)
        self.A2 = X
        Z = X.dot(self.weights.T)
        self.Z = self.sigmoid(Z)

        return self.sigmoid(Z)

    def back_prop(self, delta, alpha):
        # print(self.A.shape)
        # print(self.Z.shape)

        # error = delta.dot(self.Z.T)
        # print(self.Z.T.dot(delta.T).shape)
        # print(self.Z.shape)
        W = self.weights

        # print(self.A2.T.shape)
        self.weights += self.A2.T.dot(delta.T).T
        # print(self.A2.T.dot(delta.T).T)
        delta = np.multiply(W.T.dot(delta)[1:], self.g_prime(self.A.T))

        # print('DONE')


        return delta

    def init_weights(self, in_layer, out_layer):
        epsilon_init = 0.12
        W = np.random.rand(out_layer, in_layer + 1) * 2 * epsilon_init - epsilon_init

        return W

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def g_prime(self, a):
        return np.multiply(a, np.subtract(1, a))

    def sig_grad(self, z):
        return np.multiply(self.sigmoid(z), (1 - self.sigmoid(z)))
