" Andy "
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
        pass

    def on_update(self, elapsed):
        self.total_time += elapsed

        if self.total_time > 100:
            self.parent.change_state("Menu")

    def on_render(self, screen):
        print("Rendering")

    def on_mouse_down(self, pos):
        pass
