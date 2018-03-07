import numpy as np


class Environment():
    def create_train_cross_test(self, X, y, train_perc, cross_perc):
        m = X.shape[0]

        self.trainX = X[:int(np.floor(m*train_perc)), :]
        self.trainy = y[:int(np.floor(m*train_perc))]

        self.crossX = X[int(np.ceil(m*train_perc)):int(np.floor(m*cross_perc)), :]
        self.crossy = y[int(np.ceil(m*train_perc)):int(np.floor(m*cross_perc))]

        self.testX = X[int(np.ceil(m*cross_perc)):, :]
        self.testy = y[int(np.ceil(m*cross_perc)):]
