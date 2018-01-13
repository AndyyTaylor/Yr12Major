import pygame

from .... import config
from ....states.AbstractState import State

class MainState(State):
    " The main state for this enviroment "

    def __init__(self):
        super().__init__("Rawplot", "Enviromnents")

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        pygame.draw.rect(screen, config.RED, (50, 50, 200, 200))

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_init(self):
        pass

    def on_shutdown(self):
        pass
