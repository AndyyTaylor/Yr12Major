import numpy as np
import sys
from math import e, log

class NN():
    def __init__(self, input_layer_size, hidden_layer_size, hidden_layer2_size, hidden_layer3_size, num_labels):
        self.Theta1 = self.init_weights(input_layer_size, hidden_layer_size)
        self.Theta2 = self.init_weights(hidden_layer_size, hidden_layer2_size)
        self.Theta3 = self.init_weights(hidden_layer2_size, hidden_layer3_size)
        self.Theta4 = self.init_weights(hidden_layer3_size, num_labels)
        self.input_nodes = input_layer_size

        self.num_labels = num_labels

        self.alpha = 0.08
        self.epoch = 0

        self.print_line = ""

        self.prev_cost = 999999999

    def train(self, X, y, num_iters):

        for i in range(1):
            self.out("Epoch " + str(self.epoch) + " .. ", True)

            Theta1_grad, Theta2_grad, Theta3_grad, Theta4_grad = self.gradient(X, y)

            # numgrad = self.gradient_check(X, y, np.concatenate((self.Theta1.flatten(), self.Theta2.flatten())))
            # grad = np.concatenate((Theta1_grad.flatten(), Theta2_grad.flatten()))

            # for i in range(grad.shape[0]):
            #     print(grad[i], numgrad[i])

            self.Theta1 -= self.alpha * Theta1_grad
            self.Theta2 -= self.alpha * Theta2_grad
            self.Theta3 -= self.alpha * Theta3_grad
            self.Theta4 -= self.alpha * Theta4_grad

            cost = self.cost(X, y)
            self.epoch += 1

            if self.prev_cost < cost:
                self.alpha /= 2.0
                print("Alpha:", self.alpha)

            self.prev_cost = cost

            print("Epoch " + str(self.epoch) + " .. "  + str(self.cost(X, y)))
            self.print_line = ""

    def out(self, s, add=False):
        sys.stdout.write(self.print_line + s + "\r")
        if add: self.print_line += s
        sys.stdout.flush()

    def predict(self, x):
        output = self.feed_forward(x)

        if len(output.shape) > 1:
            return np.argmax(output, axis=1)

        return np.argmax(output)

    def feed_forward(self, x, backprop=False, Theta1=False, Theta2=False):  # Make this work with vector & matrix
        if isinstance(Theta1, bool): Theta1 = self.Theta1
        if isinstance(Theta2, bool): Theta2 = self.Theta2
        Theta3 = self.Theta3
        Theta4 = self.Theta4

        X = np.insert(x, 0, 1, axis=1)
        # print(X.shape)
        A1 = X
        Z2 = A1.dot(Theta1.T)

        # self.out('1', True)

        A2 = np.insert(self.sigmoid(Z2), 0, 1, axis=1)
        Z3 = A2.dot(Theta2.T)

        # self.out('2', True)

        A3 = np.insert(self.sigmoid(Z3), 0, 1, axis=1)
        Z4 = A3.dot(Theta3.T)

        # self.out('3', True)

        A4 = np.insert(self.sigmoid(Z4), 0, 1, axis=1)
        Z5 = A4.dot(Theta4.T)

        # self.out('4', True)

        A5 = self.sigmoid(Z5)

        # self.out('_', True)

        if backprop:
            return (A1, Z2, A2, Z3, A3, Z4, A4, Z5, A5)

        if A5.shape[0] == 2:
            return A5[1]

        return A5

    def cost(self, x, y, Theta1=False, Theta2=False):
        if isinstance(Theta1, bool): Theta1 = self.Theta1
        if isinstance(Theta2, bool): Theta2 = self.Theta2
        Theta3 = self.Theta3
        Theta4 = self.Theta4

        predicted = self.feed_forward(x, False, Theta1, Theta2)

        m = predicted.shape[0]

        J = 0
        for i in range(m):
            pred = predicted[i]
            # print(pred)
            # pred = np.ones(pred.shape) * 0.000001
            # pred[int(y[i])] = 0.999999

            # pred = np.ones(pred.shape) * 0.1
            # pred[int(y[i])] = 0.9

            lbl = np.zeros((self.num_labels, 1))
            lbl[int(y[i]), 0] = 1
            # print(np.subtract(np.multiply(-(lbl.T), (np.log(pred))), np.multiply((1 - lbl.T).T, (np.log(1-pred)))))
            J += np.sum(np.subtract(np.multiply(-(lbl.T), (np.log(pred))), np.multiply((1 - lbl.T).T, (np.log(1-pred)))))
            # print(lbl)

        J = (1.0 / m) * J

        return J

    def gradient(self, x, y, Theta1=False, Theta2=False):
        if isinstance(Theta1, bool): Theta1 = self.Theta1
        if isinstance(Theta2, bool): Theta2 = self.Theta2
        Theta3 = self.Theta3
        Theta4 = self.Theta4

        m = x.shape[0]

        Theta1_grad = np.zeros(Theta1.shape)
        Theta2_grad = np.zeros(Theta2.shape)
        Theta3_grad = np.zeros(Theta3.shape)
        Theta4_grad = np.zeros(Theta4.shape)

        for i in range(m):
            self.out(str(i))

            A1, Z2, A2, Z3, A3, Z4, A4, Z5, A5 = self.feed_forward(np.array(x[i, :]).reshape(1, self.input_nodes), True, Theta1, Theta2)

            lbl = np.zeros((self.num_labels, 1))
            lbl[int(y[i]), 0] = 1

            D5 = np.subtract(A5, lbl.T)

            D4 = np.multiply(Theta4.T.dot(D5.T)[1:], self.sig_grad(Z4.T))

            D3 = np.multiply(Theta3.T.dot(D4)[1:], self.sig_grad(Z3.T))

            D2 = np.multiply(Theta2.T.dot(D3)[1:], self.sig_grad(Z2.T))

            # print(D2.shape)

            Theta4_grad = np.add(Theta4_grad, D5.T.dot(A4))
            Theta3_grad = np.add(Theta3_grad, D4.dot(A3))
            Theta2_grad = np.add(Theta2_grad, D3.dot(A2))
            Theta1_grad = np.add(Theta1_grad, D2.dot(A1))

        Theta1_grad = (1.0 / m) * Theta1_grad
        Theta2_grad = (1.0 / m) * Theta2_grad
        Theta3_grad = (1.0 / m) * Theta3_grad
        Theta4_grad = (1.0 / m) * Theta4_grad

        return Theta1_grad, Theta2_grad, Theta3_grad, Theta4_grad

    def sigmoid(self, z):
        return np.divide(1.0, (1 + np.power(e, -z)))

    def sig_grad(self, z):
        return np.multiply(self.sigmoid(z), (1 - self.sigmoid(z)))

    def init_weights(self, in_layer, out_layer):
        """ Break symmetry """
        epsilon_init = 0.12
        W = np.random.rand(out_layer, in_layer + 1) * 2 * epsilon_init - epsilon_init

        return W
