import random
import os
import struct
import pygame
import numpy as np

from .... import config
from ....states.AbstractState import State
from ....ui.DataImage import DataImage
from ....ui.Textbox import Textbox
from ....ui.Button import Button

class MNISTHandwriting(State):
    " The main state for this enviroment "

    def __init__(self, agent):
        super().__init__("MNIST Handwritten Digits", "Environments")

        self.agent = agent
        self.m = 500

        self.x = np.zeros((self.m, 28*28))
        self.y = np.zeros((self.m, 1))

        self.viewer = DataImage(180, 20, 400, 400, 28, 28)

        self.labelText = Textbox(180, 450, 100, 100, "-", config.BLACK, 156)
        self.predText = Textbox(480, 450, 100, 100, "-", config.BLACK, 156)

        self.ind = 0
        self.training = False

        self.elements = [
            self.labelText,
            self.predText,
            # Button(20, 20, 140, 120,
            #        config.BLACK, config.WHITE,
            #        "T100x", config.BLACK, 42,
            #        lambda: self.agent.train(self.getx(), self.gety(), 100)),
            Button(20, 20, 140, 120,
                   config.BLACK, config.WHITE,
                   "T100x", config.BLACK, 42,
                   self.toggle_training),
            Button(20, 160, 140, 120,
                   config.BLACK, config.WHITE,
                   "NEXT", config.BLACK, 42,
                   lambda: self.change_digit(1)),
            Button(20, 300, 140, 120,
                   config.BLACK, config.WHITE,
                   "PREV", config.BLACK, 42,
                   lambda: self.change_digit(-1))
        ]

    def toggle_training(self):
        self.training = not self.training

    def on_update(self, elapsed):
        if self.training:
            print("Perc:", self.get_percentage())
            self.agent.train(self.getx(), self.gety(), 1)

    def on_render(self, screen):
        self.viewer.on_render(screen, self.x[self.ind, :])
        for elem in self.elements:
            elem.on_render(screen)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        i = 0
        for label, img in self.read():
            x = img.flatten()
            y = label

            self.x[i, :] = x

            self.y[i, :] = y

            i+=1

        self.change_digit()     # Load prediction

    def on_shutdown(self):
        pass

    def on_mouse_down(self, pos):
        for elem in self.elements:
            if isinstance(elem, Button) and pygame.Rect(elem.get_rect()).collidepoint(pos):
                elem.on_click()
                return

    def change_digit(self, inc=0):
        self.ind = max(min(self.ind + inc, self.m-1), 0)

        col = config.RED
        guess = int(self.agent.predict(self.x[self.ind]))
        if guess == self.y[self.ind]:
            col = config.BLUE

        self.predText.set_text(guess)
        self.predText.set_col(col)

        self.labelText.set_text(int(self.y[self.ind]))

        # cost = self.agent.cost(self.getx(), self.gety())
        # Theta1_grad, Theta2_grad = self.agent.gradient(self.getx(), self.gety())
        perc = self.get_percentage()
        # print(perc)

    def get_percentage(self):
        pred = self.agent.predict(self.getx())

        # print(pred)

        correct = 0
        for i in range(self.m):
            if pred[i] == self.y[i]:
                correct += 1

        return correct / self.m

    def getx(self):
        return self.x

    def gety(self):
        lbl = np.zeros((len(self.y), 10))
        for i in range(len(self.y)):
            lbl[i, int(self.y[i])] = 1
        return lbl

    def read(self, dataset="training", path="/Users/andytaylor/Google Drive/Major/data/datasets"):
        """
        Python function for importing the MNIST data set.  It returns an iterator
        of 2-tuples with the first element being the label and the second element
        being a numpy.uint8 2D array of pixel data for the given image.
        """

        if dataset == "training":
            fname_img = os.path.join(path, 'train-images-idx3-ubyte')
            fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
        elif dataset == "testing":
            fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
            fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')

        # Load everything in some numpy arrays
        with open(fname_lbl, 'rb') as flbl:
            magic, num = struct.unpack(">II", flbl.read(8))
            lbl = np.fromfile(flbl, dtype=np.int8)

        with open(fname_img, 'rb') as fimg:
            magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
            img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

        get_img = lambda idx: (lbl[idx], img[idx])

        # Create an iterator which returns each image in turn
        for i in range(min(len(lbl), self.m)):
            if i % 100 == 0: print("Loaded:", i)
            yield get_img(i)
