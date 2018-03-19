import numpy as np


def get_function(name):
    if name == 'sigmoid':
        return Sigmoid
    elif name == 'softmax':
        return Softmax
    elif name == 'relu':
        return ReLU
    elif name == 'tanh':
        return Tanh
    else:
        raise NotImplementedError("Function not implemented:", name)


class Sigmoid():
    def __call__(self, a):
        return 1 / (1 + np.exp(-a))

    def grad(self, a, call=False):
        if call:
            a = self.__call__(a)
        return a * (1 - a)


class Softmax():
    def __call__(self, a):
        expA = np.exp(a)
        return expA / expA.sum(axis=1, keepdims=True)

    def grad(self, a, call=False):
        if call:
            a = self.__call__(a)
        return a * (1 - a)


class Tanh():
    def __call__(self, a):
        return (np.exp(a) - np.exp(-a)) / (np.exp(a) + np.exp(-a))

    def grad(self, a, call=False):
        if call:
            a = self.__call__(a)
        return 1 - a**2


class ReLU():
    def __call__(self, a):
        return a * (a > 0)

    def grad(self, a):
        return (a > 0) * 1
