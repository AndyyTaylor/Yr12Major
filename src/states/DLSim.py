" Andy "
import pygame, random
import numpy as np

from .AbstractState import State

from ..ml.agents.deeplearning import *
from ..ml.environments import BinaryAddition as Environment


class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.environment = Environment(train_perc=0.8, cross_perc=0.0, limit=3000)
        self.agent = NeuralNetwork()
        self.agent.add_layer(Dense(48, input_shape=self.environment.num_features))
        # self.agent.add_layer(Recurrent(10, input_shape=self.environment.num_features))
        self.agent.add_layer(Activation('relu'))
        self.agent.add_layer(Dense(2))
        self.agent.add_layer(Activation('softmax'))

        self.num_iters = 3000
        self.iteration = 0

    def on_init(self):
        self.environment.init()

    def on_shutdown(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        # print(self.environment.trainX[0])
        # print(self.environment.trainy[0])

        # self.agent.cross_validate(self.environment.crossX, self.environment.crossy, self.environment.get_perc_error)

        # print(':', self.environment.get_perc_error(self.environment.testX, self.environment.testy, self.agent.predict))
        # y = self.agent.predict(self.environment.trainX)
        # correct = 0
        # for m in range(len(y)):
        #     if y[m] == self.environment.trainy[m]:
        #         correct += 1
        # print("Train Accuracy:", correct / len(y))
        #
        y = self.agent.feed_forward(self.environment.testX)
        print(y[0, 0, :])
        y = self.agent.predict(self.environment.testX)
        print(y[0, 0])
        # correct = 0
        # for m in range(len(y)):
        #     if y[m] == self.environment.testy[m]:
        #         correct += 1
        # print("Test Accuracy:", correct / len(y))
        # print(y)

    def on_render(self, screen):
        self.environment.on_render(screen, self.agent.predict)

    def on_mouse_event(self, event):
        pass

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            self.auto_turns = not self.auto_turns
