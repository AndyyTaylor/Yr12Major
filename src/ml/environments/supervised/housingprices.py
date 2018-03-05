import pygame
import numpy as np

from . import preprocessing as pp


class HousingPrices():
    def __init__(self):
        pp.load_file("housing-prices/train.csv")

        self.num_features = 1

    def on_render(screen):
        pass
