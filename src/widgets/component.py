
import pygame
import numpy as np

from src import config
from .frame import Frame


class Component(Frame):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, False, config.SCHEME4)

        self.slot_width = 40
        self.slot_height = 30

        self.inputs = []
        self.input_pos = []
        self.input_labels = []
        self.outputs = []
        self.output_pos = []
        self.output_labels = []

    def setup_inputs_and_outputs(self):
        return  # STUBBY


