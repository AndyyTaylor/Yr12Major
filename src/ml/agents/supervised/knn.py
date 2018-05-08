import sys
import numpy as np
from sortedcontainers import SortedList
from scipy.spatial import distance

# Shit to implement in other codes:
# i, x in enumerate(X)
# dict.get()


class KNN():
    def __init__(self, _, k=4):  # in knn we don't care about the number of features
        # self.k_determined = (k is not None)

        # if k is None:
        #     self.k = 1
        # else:
        #     self.k = k
        self.k = k

    def train(self, X, y):
        self.X = X
        self.y = y

    def cross_validate(self, X, y, score):
        if not self.k_determined:
            sys.stdout.flush()

            best_score = float('-inf')
            while True:
                print("Determining k ..", self.k, end='\r')
                current_score = score(X, y, self.predict)
                print(current_score)
                # if current_score < best_score and self.k > 15:
                if self.k > 15:
                    self.k -= 1
                    break

                best_score = current_score
                self.k += 1

            print("Determining k ..", self.k)
            print(self.k)
            self.k_determined = True

    def predict(self, X):
        y = np.zeros(len(X))  # vector containing labels
        for i, x in enumerate(X):  # test points
            sl = SortedList()
            for j, xt in enumerate(self.X):  # train points
                # diff = x - xt
                # dist = diff.dot(diff)  # squared difference
                dist = distance.euclidean(x, xt)

                if len(sl) < self.k:
                    sl.add((dist, self.y[j]))   # add tuple(distance, class)
                else:
                    if dist < sl[-1][0]:  # last element of sl is largest distance, first element of tuple is its distance
                        del sl[-1]  # remove worst point as we only want k neighbours
                        sl.add((dist, self.y[j]))  # add if this point is closer

            y[i] = self._predict(sl)

        return y


class ClassificationKNN(KNN):
    def _predict(self, sl):
        # Count votes by class to determine prediction
        votes = {}
        for _, v in sl:  # we don't care about the distance anymore
            votes[v] = votes.get(v, 0) + 1  # super nice function - if v doesn't exist it returns 0

        max_votes = 0
        best_class = 0
        for v, count in votes.items():
            if count > max_votes:
                max_votes = count
                best_class = v

        return best_class


class RegressionKNN(KNN):
    def _predict(self, sl):
        values = []
        for _, v in sl:
            values.append(float(v))

        return np.mean(values)
