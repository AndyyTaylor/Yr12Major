" Andy "
import pygame, random
import numpy as np

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
# from ..ml.agents.deeplearning.layers import Dense
from ..ml.agents import ClassificationKNN as Agent
# from ..ml.environments import MNIST as Environment
from ..ml.environments import StockPrices as Environment


class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.environment = Environment()
        self.agent = Agent(self.environment.num_features)

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
        self.agent.train(self.environment.trainX, self.environment.trainy)

        self.agent.cross_validate(self.environment.crossX, self.environment.crossy, self.environment.get_perc_error)

        print(':', self.environment.get_perc_error(self.environment.testX, self.environment.testy, self.agent.predict))

    def rmsle(self, y_true, y_pred):
        y_true = np.exp(y_true)
        y_pred = np.exp(y_pred)

        assert len(y_true) == len(y_pred)
        return np.square(np.log(y_pred + 1) - np.log(y_true + 1)).mean() ** 0.5

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_event(self, event):
        pass

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            self.auto_turns = not self.auto_turns
