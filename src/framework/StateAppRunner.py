" App runner "

import datetime
import pygame
from .. import config
from pygame.locals import DOUBLEBUF
from .StateRegistry import StateRegistry
from .StateGroup import StateGroup
from ..screens import MainMenu, LevelSelector, Level


class StateAppRunner():
    _instance = None

    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
                                              DOUBLEBUF)
        self.window.set_alpha(None)
        pygame.display.set_caption("Andy's Machine Learning")
        self.last_update = datetime.datetime.now()

        StateRegistry.instance().set_screen(self.window)

        # Fix stategroup order
        master_group = StateGroup("MasterState")
        StateRegistry.instance().register_group(master_group)

        MainMenu()
        LevelSelector()
        Level()

        master_group.change_state("MainMenu")

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
        master_state = StateRegistry.instance().get_group("MasterState")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                master_state.on_mouse_motion(event, pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    master_state.on_scroll(int(event.button == 5))
                else:
                    pos = pygame.mouse.get_pos()
                    master_state.on_mouse_down(event, pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                master_state.on_mouse_up(event, pos)
            elif event.type == pygame.KEYDOWN:
                master_state.on_key_down(event.key)

    def update(self, elapsed):
        StateRegistry.instance().get_group("MasterState").on_update(elapsed)

    def render(self):
        StateRegistry.instance().get_group("MasterState").on_render(self.window)

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
