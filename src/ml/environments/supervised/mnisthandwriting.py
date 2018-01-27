import random
import os
import struct
import numpy as np

from ....states.AbstractState import State
from ....ui.DataImage import DataImage

class MNISTHandwriting(State):
    " The main state for this enviroment "

    def __init__(self):
        super().__init__("MNIST Handwritten Digits", "Environments")

        self.x = np.zeros((0, 28*28))
        self.y = np.zeros((0, 1))

        for label, img in self.read():
            x = img.flatten()
            y = label

            self.x = np.vstack((self.x, x))
            self.y = np.vstack((self.y, y))

        self.ind = 0
        self.viewer = DataImage(50, 50, 500, 500, 28, 28)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.viewer.on_render(screen, self.x[self.ind, :])
        print(self.y[self.ind])

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_mouse_down(self, pos):
        self.ind += 1

    def getx(self):
        return self.x

    def gety(self):
        return self.y


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
        for i in range(min(len(lbl), 5)):
            yield get_img(i)
