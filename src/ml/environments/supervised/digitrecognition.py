import pandas as pd
import numpy as np

from .... import config


class DigitRecognition():
    def __init__(self, limit=2000):
        self.X, self.y = self.get_data(limit)

        self.create_train_test(self.X, self.y, 0.8)

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

    def create_train_test(self, X, y, ratio):
        m = X.shape[0]

        self.trainX = X[:int(np.floor(m*ratio)), :]
        self.trainy = y[:int(np.floor(m*ratio))]

        self.testX = X[int(np.ceil(m*ratio)):, :]
        self.testy = y[int(np.ceil(m*ratio)):]

    def get_perc_error(self, predict):
        pred = predict(self.testX)
        return np.mean(pred == self.testy)

    def on_render(self, screen):
        pass
