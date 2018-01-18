" Andy "
from .AbstractState import State

from ..ml.environments.lineardataset.MainState import MainState as Environment
from ..ml.agents.linearregression.LinearRegression import LinearRegression as Agent

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.total_time = 0

        self.environment = Environment()
        self.agent = Agent()

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.environment.on_render(screen)
        self.agent.on_render(screen, self.environment.plot)

    def on_mouse_down(self, pos):
        pass
