" Andy "
from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
from ..ml.environments.lineardataset.MainState import MainState as Environment
from ..ml.agents import LinearRegression as Agent
from ..ml.environments.supervised import envconfig

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.total_time = 0

        self.environment = Environment(envconfig)
        self.agent = Agent(envconfig.n)

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        self.agent.on_update(self.environment.getx(), self.environment.gety())

    def on_render(self, screen):
        self.environment.on_render(screen)
        self.agent.on_render(screen, self.environment.plot)

    def on_mouse_down(self, pos):
        self.environment.on_mouse_down(pos)
