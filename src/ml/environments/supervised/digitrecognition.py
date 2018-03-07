import pandas as pd
import numpy as np

from .... import config
from .environment import Environment


class DigitRecognition(Environment):
    def __init__(self, limit=2000):
        self.X, self.y = self.get_data(limit)

        self.create_train_cross_test(self.X, self.y, 0.6, 0.8)

        self.num_features = self.X.shape[1]

    def get_data(self, limit=None):
        df = pd.read_csv(config.DATASET_PATH + "digit-recognition/train.csv")
        data = df.as_matrix()

        np.random.shuffle(data)

        # first column is the labels
        X = data[:, 1:] / 255.0  # scale data
        y = data[:, 0]

        if limit is not None:
            X = X[:limit]
            y = y[:limit]

        return X, y

    def get_perc_error(self, X, y, predict):
        pred = predict(X)
        return np.mean(pred == y)

    def on_render(self, screen):
        pass
