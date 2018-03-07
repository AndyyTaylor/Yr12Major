from scipy.stats import skew
import numpy as np
import pandas as pd
import math

from .... import config
from .environment import Environment
from . import preprocessing as pp


class HousingPrices(Environment):
    def __init__(self, limit=None):
        super().__init__()

        # self.X, self.y = self.get_data(limit)
        # self.X, self.y = self.transform_data(self.X, self.y)
        self.X, self.y = pp.load_file("housing-prices/train.csv")

        self.create_train_cross_test(self.X, self.y, 0.6, 0.8)

        self.num_features = self.X.shape[1]

    def get_data(self, limit=None):
        df = pd.read_csv(config.DATASET_PATH + "housing-prices/train.csv")
        data = df.as_matrix()

        np.random.shuffle(data)

        X = data[:, :-1]
        y = data[:, -1]

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
        y = np.exp(y)
        predictions = np.exp(predict(X))
        perc = np.divide(np.subtract(predictions, y), y) * 100
        return 100 - np.abs(perc).mean()
