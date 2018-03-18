" Andy "
import pygame, random
import numpy as np

from .AbstractState import State

from ..ml.agents.deeplearning import *
from ..ml.environments import DigitRecognition as Environment


class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.environment = Environment(train_perc=0.8, cross_perc=0.0, limit=3000)
        self.agent = NeuralNetwork()
        self.agent.add_layer(Dense(512, input_shape=self.environment.num_features))
        self.agent.add_layer(Activation('sigmoid'))
        self.agent.add_layer(Dense(215))
        self.agent.add_layer(Activation('sigmoid'))
        self.agent.add_layer(Dense(10))
        self.agent.add_layer(Activation('softmax'))

        self.num_iters = 3000
        self.iteration = 0

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        self.agent.back_propagate(self.environment.trainX, self.environment.trainy)

        # self.agent.cross_validate(self.environment.crossX, self.environment.crossy, self.environment.get_perc_error)

        # print(':', self.environment.get_perc_error(self.environment.testX, self.environment.testy, self.agent.predict))
        y = self.agent.predict(self.environment.trainX)
        correct = 0
        for m in range(len(y)):
            if y[m] == self.environment.trainy[m]:
                correct += 1
        print("Train Accuracy:", correct / len(y))

        y = self.agent.predict(self.environment.testX)
        correct = 0
        for m in range(len(y)):
            if y[m] == self.environment.testy[m]:
                correct += 1
        print("Test Accuracy:", correct / len(y))
        # print(y)

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_event(self, event):
        pass

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            self.auto_turns = not self.auto_turns
