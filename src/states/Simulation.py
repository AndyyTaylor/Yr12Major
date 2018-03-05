" Andy "
import pygame, random
import numpy as np

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
# from ..ml.agents.deeplearning.layers import Dense
from ..ml.agents import LinearRegression as Agent
# from ..ml.environments import MNIST as Environment
from ..ml.environments import HousingPrices as Environment


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
        self.agent.train(self.environment.trainX, self.environment.trainy, self.num_iters)

        self.iteration += self.num_iters

        print("-" * 30)
        print("Iteration", self.iteration)
        print("Cost:", self.agent.cost(np.insert(self.environment.trainX, 0, 1, axis=1), self.environment.trainy, len(self.environment.trainy)))
        print("Rmsle:", self.rmsle(self.environment.testy, self.agent.predict(self.environment.testX)))
        print("Train Perc Error:", self.environment.perc_error(self.agent.predict))
        print("Test  Perc Error:", self.environment.perc_error(self.agent.predict, dataset='test'))

        examples = np.random.randint(0, high=len(self.environment.testy), size=5)
        predictions = self.agent.predict(self.environment.testX)
        for i in examples:
            print(int(predictions[i]), "->", int(self.environment.testy[i]))

    def rmsle(self, y_true, y_pred):
        print(y_true.shape)
        print(y_pred.shape)
        assert len(y_true) == len(y_pred)
        return np.square(np.log(y_pred + 1) - np.log(y_true + 1)).mean() ** 0.5

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_event(self, event):
        pass

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            self.auto_turns = not self.auto_turns
