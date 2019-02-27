import sys
import numpy as np
from sortedcontainers import SortedList
from scipy.spatial import distance

# Shit to implement in other codes:
# i, x in enumerate(X)
# dict.get()


class KNN():
    def __init__(self, _, k=1):  # in knn we don't care about the number of features
        # self.k_determined = (k is not None)
        #
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
        y = np.zeros(len(X))  # vector (array) containing labels (answers)
        for i, x in enumerate(X):  # test points to create predictions for
            sl = SortedList()
            for j, xt in enumerate(self.X):  # training points
                # Get the 'difference' between the two samples
                dist = distance.euclidean(x, xt)

                if len(sl) < self.k: # If don't have k points yet
                    sl.add((dist, self.y[j]))   # add tuple(distance, class)
                else:
                    # last element of sl is largest 'difference',
                    # first element of tuple is its distance
                    if dist < sl[-1][0]:
                        del sl[-1]  # remove worst point as we only want k best points
                        sl.add((dist, self.y[j]))  # add as this point is closer

            y[i] = self._predict(sl)

        return y


class ClassificationKNN(KNN):
    def _predict(self, sl):
        # Takes in a list of tuples (distance, value)
        # Returns the most commonly occuring value

        # Count votes by class to determine prediction
        votes = {}
        for _, value in sl:  # we don't care about the distance anymore
            votes[value] = votes.get(value, 0) + 1  # if value doesn't exist it returns 0

        # Basically a findMax for a dictionary
        max_votes = 0
        best_class = 0
        for value, count in votes.items():
            if count > max_votes:
                max_votes = count
                best_class = value

        return best_class


class RegressionKNN(KNN):
    def _predict(self, sl):
        values = []
        for _, v in sl:
            values.append(float(v))

        return np.mean(values)
