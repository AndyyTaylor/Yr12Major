" Main Menu "

from .. import config
from .AbstractState import State
from ..ui.Rectangle import Rectangle
from ..ui.Button import Button

class MainMenu(State):
    " A "

    def __init__(self):
        super().__init__("Main", "Menu")

        self.total_time = 0
        self.elements = [
            Rectangle(0, 0, 100, 100, config.BLUE),
            Button(300, 300, 50, 50, lambda: self.parent.change_state("IntroGroup"))
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

        if self.total_time > 3000:
            print("Clicking button")
            self.elements[1].on_click()

    def on_render(self, screen):
        for elem in self.elements:
            elem.on_render(screen)
