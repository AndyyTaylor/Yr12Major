" Main Menu "

from .. import config
from .AbstractState import State
from ..ui.Rectangle import Rectangle
from ..ui.Button import Button
from ..ui.Textbox import Textbox

class MainMenu(State):
    " A "

    def __init__(self):
        super().__init__("Main", "Menu")

        self.total_time = 0
        self.elements = [
            Textbox(100, 10, 400, 50, "What would you like to see today?", config.GRAY, 24),
            Button(100, 250, 400, 400,
                   config.BLACK, config.WHITE,
                   "Begin", config.BLACK,
                   lambda: self.parent.change_state("Environments"))
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
            # self.elements[1].on_click()

    def on_render(self, screen):
        for elem in self.elements:
            elem.on_render(screen)

    def on_mouse_down(self, pos):
        self.elements[1].on_click()
