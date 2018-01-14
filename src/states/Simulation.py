" Andy "
from .AbstractState import State

from ..ml.environments.lineardataset.MainState import MainState as Environment

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.total_time = 0

        self.environment = Environment()

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        print("Intro state entered")

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_down(self, pos):
        pass
