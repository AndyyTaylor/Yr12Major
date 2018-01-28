import numpy as np
from math import e, log

class NN():
    def __init__(self, input_layer_size, hidden_layer_size, num_labels):
        self.Theta1 = self.init_weights(input_layer_size, hidden_layer_size)
        self.Theta2 = self.init_weights(hidden_layer_size, num_labels)

        self.num_labels = num_labels

    def train(self, X, y, num_iters):
        print("Trained " + str(num_iters) + " times")

    def predict(self, x):
        output = self.feed_forward(x)

        if len(output.shape) > 1:
            return np.argmax(output, axis=1)

        return np.argmax(output)

    def feed_forward(self, x, backprop=False):  # Make this work with vector & matrix
        X = np.insert(x, 0, 1, axis=1)

        A1 = X
        Z2 = A1.dot(self.Theta1.T)

        A2 = np.insert(self.sigmoid(Z2), 0, 1, axis=1)
        Z3 = A2.dot(self.Theta2.T)

        A3 = self.sigmoid(Z3)

        if A3.shape[0] == 2:
            return A3[1]

        if backprop:
            return (A1, Z2, A2, Z3, A3)

        return A3

    def cost(self, x, y):
        predicted = self.feed_forward(x)
        print(predicted.shape)
        m = predicted.shape[0]

        J = 0
        for i in range(1):
            pred = predicted[i]

            lbl = np.zeros((self.num_labels, 1))
            lbl[int(y[i]), 0] = 1

            J += np.sum(np.subtract(np.multiply(-(lbl.T), (np.log(pred))), np.multiply((1 - lbl.T).T, (np.log(1-pred)))))
            # print(lbl)

        J = (1.0 / m) * J

        return J

    def gradient(self, x, y):
        m = x.shape[0]

        Theta1_grad = np.zeros(self.Theta1.shape)
        Theta2_grad = np.zeros(self.Theta2.shape)

        for i in range(1):
            A3 = self.feed_forward(x) # Take all params

            lbl = np.zeros((self.num_labels, 1))
            lbl[int(y[i]), 0] = 1

            D3 = np.subtract(A3, lbl.T)

            D2 = np.multiply(self.Theta2.dot(D3.T), self.sig_grad(Z2.T)

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def init_weights(self, in_layer, out_layer):
        """ Break symmetry """
        epsilon_init = 0.12
        W = np.random.rand(out_layer, in_layer + 1) * 2 * epsilon_init - epsilon_init

        return W
