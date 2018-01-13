" Main Menu "

from .. import config
from .AbstractState import State
from ..ui.Rectangle import Rectangle

class MainMenu(State):
    " A "

    def __init__(self):
        super().__init__("Main", "Menu")

        self.total_time = 0
        self.elements = [
            Rectangle(0, 0, 100, 100, config.BLUE)
        ]

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
        print("Main Menu")

    def on_render(self, screen):
        for elem in self.elements:
            elem.on_render(screen)
