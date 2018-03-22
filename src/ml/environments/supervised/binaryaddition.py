import numpy as np
import random
from .environment import Environment


# The first n_bits samples will be a part of the same sequence.
# The states in the RNN will then be reset, I still have to think of a way to signal this


class BinaryAddition(Environment):
    def __init__(self, limit=1000, train_perc=0.6, cross_perc=0.2):
        super().__init__()

        if limit is None:
            limit = 10000

        n_bits = 8
        n_numbers = 2
        self.num_features = n_numbers
        self.num_classes = 2

        self.X = np.zeros((limit, n_bits+1, n_numbers))
        self.y = np.zeros((limit, n_bits+1))

        for m in range(limit):
            a = '0'
            b = '0'
            for bit in range(n_bits):
                a += random.choice(['0', '1'])
                b += random.choice(['0', '1'])

            c = int(a, 2) + int(b, 2)
            c = f'{c:08b}'
            if len(c) == n_bits:
                c = '0' + c

            for bit in range(n_bits, -1, -1):
                self.X[m, (n_bits - bit)] = np.array([int(a[bit]), int(b[bit])])
                self.y[m, (n_bits - bit)] = int(c[bit])

        self.trainX = self.X[:int((limit*0.8)) - int((limit*0.8)) % 9]
        self.trainy = self.y[:int((limit*0.8)) - int((limit*0.8)) % 9]

        self.testX = self.X[int((limit*0.8)) - int((limit*0.8)) % 9:]
        self.testy = self.y[int((limit*0.8)) - int((limit*0.8)) % 9:]

    def on_render(self, screen, predict):
        pass
