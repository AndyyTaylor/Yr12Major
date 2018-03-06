import numpy as np
import csv

DATASET_PATH = "/Users/andytaylor/Google Drive/Major/data/datasets/"


class Numerical():
    def __init__(self):
        self.vals = []

    def add_val(self, val):
        self.vals.append(float(val))

    def process(self):
        self.vals = np.log(np.array(self.vals))
        self.vals[np.isneginf(self.vals)] = 0
        self.vals = np.divide(np.subtract(self.vals, self.vals.mean()), self.vals.std())

        return self.vals


class Categorical():
    def __init__(self):
        self.vals = []

    def add_val(self, val):
        self.vals.append(val)

    def process(self):
        keys = list(set(self.vals))
        old_vals = self.vals

        self.vals = np.zeros((len(self.vals), len(keys)))
        for i in range(len(old_vals)):
            self.vals[i] = self.one_hot(keys, old_vals[i])

        return self.vals

    def one_hot(self, keys, val):
        a = np.zeros(len(keys))
        a[keys.index(val)] = 1

        return a


def load_file(file_name):  # Seperate to lead csv text etc based on extension
    with open(DATASET_PATH + file_name, 'r') as f:
        reader = csv.reader(f)
        all_examples = [row for row in reader]

        headers = all_examples.pop(0)

        holders = [False for f in range(len(all_examples[0]))]

        i = 0
        while False in holders:
            for f in range(len(all_examples[i])):
                feature = all_examples[i][f]
                if is_float(feature):
                    holders[f] = Numerical()
                elif feature == "NA" and not holders[f]:
                    holders[f] = False
                else:
                    holders[f] = Categorical()
            i += 1

            if i >= len(all_examples):
                break

        for example in all_examples:
            for f in range(len(example)):
                try:
                    holders[f].add_val(example[f])
                except ValueError:
                    holders[f].add_val(0)

        holders.pop(0)
        y = holders.pop()

        X = np.zeros((len(all_examples), 1))
        for i in range(len(holders)):
            v = holders[i].process()

            if len(v.shape) < 2:
                X = np.hstack((X, v.T.reshape((X.shape[0], 1))))
            else:
                X = np.hstack((X, v))
        X = X[:, 1:]

        return (X, np.array(np.log(y.vals)).reshape((X.shape[0], 1)))


def is_float(val):
    try:
        float(val)
        return True
    except ValueError:
        return False
