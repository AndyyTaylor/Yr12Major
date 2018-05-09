
import pygame
import numpy as np
from .component import Component
from .component import Holder
from .. import config
from ..ui.Textbox import Textbox
from src.ml.environments.game import *


class Sample:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.progress = 0


class ColorInput(Component):

    def __init__(self, num_colors):
        super().__init__(0, 0, 200, 150)
        self.text = Textbox(self.x, self.y, self.w, 40, "Colour", config.SCHEME1, 32)
        self.environment = ColorEnv(num_colors)

        self.index = {
            'train': 0,
            'cross': 0,
            'test': 0
        }

        self.colors = [config.RED, config.GREEN, config.BLUE, config.YELLOW, config.WHITE][:num_colors]

        self.output_pos.append((self.x + self.w - self.slot_width, self.y + self.h/2 - self.slot_height/2))

        self.setup_inputs_and_outputs()

        for i in range(self.environment.testX.shape[0]):
            sample = Sample(self.environment.testX[i], self.environment.testy[i])
            self.outputs[0].add_data(sample)

    def on_render(self, screen):
        super().on_render(screen)

        row_width = 110/1.2
        num_rows = int(np.sqrt(len(self.colors)))+1

        for yy in range(num_rows):
            for xx in range(num_rows):

                if yy * np.floor(num_rows) + xx >= len(self.colors):
                    break

                color = self.colors[int(yy * np.floor(num_rows) + xx)]

                pygame.draw.rect(screen, color, (self.x+20+(row_width*1.2//num_rows)*xx, self.y+40+(row_width*1.2//num_rows)*yy, (row_width//num_rows), (row_width//num_rows)))

        self.text.on_render(screen)

    def render_data(self, screen, x, y, data, size=20):
        if hasattr(data, 'y'):
            label = int(data.y)
        else:
            label = int(data)

        pygame.draw.circle(screen, self.colors[label-1], (int(x), int(y)), size)

    def get_train_data(self):
        return (self.environment.trainX, self.environment.trainy)

    def get_labels(self):
        return self.environment.get_labels()
