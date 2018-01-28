import random

class NN():
    def __init__(self):
        pass

    def train(self, X, y, num_iters):
        print("Trained " + str(num_iters) + " times")

    def predict(self, x):
        print("Predicting a number")
        return random.randint(1, 10)
