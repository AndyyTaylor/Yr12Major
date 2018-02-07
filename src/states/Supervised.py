" Andy "
import pygame

from .AbstractState import State

# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment

from ..ml.agents import LinearRegression as Agent
from ..ml.environments import LinearPlot as Environment

# from ..ml.agents import LogisticRegression as Agent
# from ..ml.environments import ClassPlot as Environment

class Supervised(State):
    " A "

    def __init__(self):
        super().__init__("Supervised", "MasterState")

        # self.agent = Agent(28*28, 512, 254, 50, 10)
        self.agent = Agent(5)   # n
        self.environment = Environment(10, 5)   # m, n

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        self.environment.on_init()

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        self.environment.on_update(elapsed)
        self.agent.train(self.environment.getx(), self.environment.gety())

    def on_render(self, screen):
        self.environment.on_render(screen, self.agent)

    def on_mouse_down(self, pos):
        self.environment.on_mouse_down(pos)

    def on_key_down(self, key):
        self.environment.on_key_down(key)
