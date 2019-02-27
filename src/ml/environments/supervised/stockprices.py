from scipy.stats import skew
import numpy as np
import pandas as pd
import math

from .... import config
from .environment import Environment
from . import preprocessing as pp


class StockPrices(Environment):
    def __init__(self, limit=None):
        super().__init__()

        self.X, self.y = self.get_data(limit)
        # self.X, self.y = self.transform_data(self.X, self.y)

        self.create_train_cross_test(self.X, self.y, 0.8, 1)

        self.num_features = self.X.shape[1]

    def get_data(self, limit=None):
        df = pd.read_csv(config.DATASET_PATH + "stocks/NAB.AX.csv")
        data = df.as_matrix()

        num = 700
        X = np.zeros((1, num))
        y = []

        past = []
        for row in data:
            if np.isnan(row[5]):
                past = []
            else:
                past.append(row[5])

            if len(past) > num:
                X = np.vstack((X, np.array(past[:-1])))
                y.append(int(past[-1] > past[-2]))
                past.pop(0)

        X = X[1:, :]

        print(len(y))
        print(y.count(1))

        if limit is not None:
            X = X[:limit]
            y = y[:limit]

        return X, y

    def transform_data(self, X, y):
        if skew(y) > 1.5:  # find a good val for this
            y = np.array([np.log(x) for x in y])  # dumb errors makes for dumb code
            self.transforms['log'] = self.transforms.get('log', []).append('y')

        return X, y

    def get_perc_error(self, X, y, predict):
        pred = predict(X)
        return np.mean(pred == y)

    # def get_perc_error(self, X, y, predict):
    #     y = np.exp(y)
    #     predictions = np.exp(predict(X))
    #     perc = np.divide(np.subtract(predictions, y), y) * 100
    #     return 100 - np.abs(perc).mean()
