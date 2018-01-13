" Intro "
from .AbstractState import State

class IntroState(State):
    " A "

    def __init__(self):
        super().__init__("Intro", "IntroGroup")

        self.total_time = 0

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        print("Intro state entered")

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        self.total_time += elapsed
        print("Intro state: " + str(self.total_time))

        if self.total_time > 100:
            self.parent.change_state("Game")

    def on_render(self):
        print("Rendering")
