# import pygame

class DataHandler:
    def __init__(self):
        self.data = []

    def add_data_point(self, x, y):
        self.data.append([x, y])

    def clear_data(self):
        self.data = []
