import pygame
import numpy as np

from . import preprocessing as pp


class HousingPrices():
    def __init__(self):
        self.X, self.y = pp.load_file("housing-prices/train.csv")
        self.m = len(self.y)

        self.trainX = self.X[:int(np.ceil(self.m * 0.6))]
        self.crossX = self.X[int(np.floor(self.m * 0.6)):int(np.ceil(self.m * 0.8))]
        self.testX = self.X[int(np.floor(self.m * 0.8)):]

        self.trainy = self.y[:int(np.ceil(self.m * 0.6))]
        self.crossy = self.y[int(np.floor(self.m * 0.6)):int(np.ceil(self.m * 0.8))]
        self.testy = self.y[int(np.floor(self.m * 0.8)):]

        self.num_features = self.X.shape[1]

    def on_render(self, screen):
        pass

    def perc_error(self, predict, dataset='train'):
        if dataset == 'train':
            X = self.trainX
            y = self.trainy
        elif dataset == 'cross':
            X = self.crossX
            y = self.crossy
        else:
            X = self.testX
            y = self.testy

        predictions = predict(X)
        perc = np.subtract(1, np.divide(predictions, y.T))
        return np.abs(perc).mean()
