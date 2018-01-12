" Intro "
from AbstractState import State

class IntroState(State):
    " A "

    def __init__(self):
        super().__init__("Intro")

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        print("Intro state entered")

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        print("Updated")

    def on_render(self):
        print("Rendering")
