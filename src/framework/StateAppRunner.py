" App runner "

import datetime
import pygame
from .. import config

from .StateRegistry import StateRegistry
from ..stategroups.StateGroup import StateGroup
from ..states.IntroState import IntroState
from ..states.MainMenu import MainMenu
from ..states.PlaceHolderEnv import PlaceHolder

class StateAppRunner():
    _instance = None

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 0, 32)
        self.last_update = datetime.datetime.now()

        StateRegistry.instance().register_group(StateGroup("MasterState"))
        StateRegistry.instance().register_group(StateGroup("IntroGroup"))
        StateRegistry.instance().register_group(StateGroup("Menu"))
        StateRegistry.instance().register_group(StateGroup("Environments"))
        IntroState()
        MainMenu()
        PlaceHolder()

        print(StateRegistry.instance().get_state("Intro").parent.name)

        self.closed = False
        self.now = None
        self.elapsed = None

    def run_loop(self):
        self.read_input()

        self.now = datetime.datetime.now()
        self.elapsed = (self.now - self.last_update).total_seconds() * 1000
        self.last_update = self.now
        self.update(self.elapsed)

        self.render()

    def read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                StateRegistry.instance().get_group("MasterState").on_mouse_down(pos)

    def update(self, elapsed):
        StateRegistry.instance().get_group("MasterState").on_update(elapsed)

    def render(self):
        self.screen.fill(config.WHITE)

        StateRegistry.instance().get_group("MasterState").on_render(self.screen)

        pygame.display.update()

    def close(self):
        # Send on_exit events
        self.closed = True

    def is_closed(self):
        return self.closed

    @staticmethod
    def instance():
        if not StateAppRunner._instance:
            StateAppRunner._instance = StateAppRunner()

        return StateAppRunner._instance
