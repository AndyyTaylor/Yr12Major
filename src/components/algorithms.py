
import pygame
from ..ui.UIElement import UIElement
from ..ui import *
from .. import config
from .component import Component
from src.ml.agents import *


class KNN(Component):

    def __init__(self, labels, render_data):
        super().__init__(0, 0, 200, 150)
        self.labels = labels
        self.render_data = render_data

        self.text = Textbox(self.x, self.y, self.w, 40, "KNN", config.SCHEME1, 32)
        self.algorithm = ClassificationKNN(0)

        self.input_pos.append((self.x, self.y + self.h/2 - self.slot_height/2))
        slot_x = self.x + self.w - self.slot_width
        for i, label in enumerate(labels):
            self.output_pos.append((slot_x, self.y - self.slot_height/2 + self.h/(labels.shape[0]+1)*(i+1)))
            self.output_labels.append(label)

        self.setup_inputs_and_outputs()

    def train(self, trainX, trainy):
        self.algorithm.train(trainX, trainy)

    def on_render(self, screen):
        super().on_render(screen)

        self.text.on_render(screen)

    def on_update(self, elapsed):
        super().on_update(elapsed)

        in_holder = self.inputs[0]
        out_holder = self.outputs[0]
        if in_holder.has_data():
            sample = in_holder.take_data()
            predicted_label = int(self.algorithm.predict(np.array([sample.x])))
            self.outputs[predicted_label].add_data(sample)
