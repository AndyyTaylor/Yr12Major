" Andy "
import pygame

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
from ..ml.agents import QLearn
from ..ml.environments import CatchApples as Environment

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.agent = QLearn(2, 2)

        self.tick_rate = 1

        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        pass

    def on_mouse_down(self, pos):
        pass

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            if self.tick_rate == 1000:
                self.tick_rate = 1
            else:
                self.tick_rate = 1000
