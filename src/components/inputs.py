
import pygame

from src import config
from ..widgets import Label, Component
from src.ml.environments.game import ColorEnv


class Sample:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.progress = 0


class ColorInput(Component):

    def __init__(self, x, y, num_colors):
        super().__init__(x, y, 280, 150)

        self.add_child(Label(0, 0, self.w, 40, config.SCHEME4, "Colour", 32, config.SCHEME1))
        self.environment = ColorEnv(num_colors)

        self.index = {
            'train': 0,
            'cross': 0,
            'test': 0
        }

        self.colors = [config.RED, config.GREEN,
                       config.BLUE, config.YELLOW, config.WHITE][:num_colors]

        self.output_pos.append((self.x + self.w - self.slot_width, self.y + self.h/2))

        self.setup_inputs_and_outputs()

        for i in range(self.environment.testX.shape[0]):
            sample = Sample(self.environment.testX[i], self.environment.testy[i])  # noqa
            # self.outputs[0].add_data(sample)

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
