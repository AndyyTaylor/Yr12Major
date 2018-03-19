import numpy as np
from .environment import Environment
from ....ui import ClassPlot


class XOR(Environment):
    def __init__(self, limit=2000, train_perc=0.6, cross_perc=0.2):
        super().__init__()

        self.num_features = 2

        self.limit = limit
        self.plot = ClassPlot(2)

        self.X = []
        self.y = []

        self.x_origin = 1.5
        self.y_origin = 1.5

        for i in range(limit):
            x = np.random.random()
            y = np.random.random()
            self.X.append([x, y])

            if not (np.round(x) == np.round(y)):
                self.y.append(0)
            else:
                self.y.append(1)

        self.X = np.array(self.X)
        self.y = np.array(self.y)
        self.X, self.y = self.unison_shuffled_copies(self.X, self.y)

        self.create_train_cross_test(self.X, self.y, train_perc, train_perc + cross_perc)

    def on_render(self, screen, predict):
        self.plot.render(screen, self.X, self.y, predict)

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]
