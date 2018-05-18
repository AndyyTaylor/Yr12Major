
import pygame
import numpy as np

from src import config
from ..components import *
from ..elements import Textbox
from src.framework.StateRegistry import StateRegistry


class Screen():
    " The abstract class that all states inherit "

    def __init__(self, name, parent):
        self.name = name
        self.parent = StateRegistry.instance().register(self, parent)

        self.components = []

        self.fps = Textbox(1300, 10, 140, 80, "00", config.BLACK, 72)

    def on_init(self):
        " Called when the application is run "
        return

    def on_shutdown(self):
        " Called when the application is closed "
        return

    def on_enter(self, data, screen, arr=None):
        pygame.draw.rect(screen, config.SCHEME5, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        if arr is None:
            arr = self.components

        arr += [self.fps]
        for comp in arr:
            comp.changed = True

    def on_exit(self):
        " Called when the state is exited "
        return

    def on_update(self, elapsed):
        for comp in self.components + [self.fps]:
            comp.on_update(elapsed)

        self.fps.set_text(str(int(1000 / elapsed)))

    def on_render(self, screen, components=None):
        if components is None:
            components = self.components

        changed_rectangles = []
        for comp in components + [self.fps]:

            if comp.has_changed():
                changed_rectangles.append((comp.get_prev_rect(), comp.back_color or config.SCHEME5))

        for rect in changed_rectangles:
            pygame.draw.rect(screen, rect[1], rect[0])

        for comp in components + [self.fps]:
            if comp.has_changed():
                comp.on_render(screen)

    def on_key_down(self, key):
        return

    def on_mouse_event(self, event):
        return

    def on_mouse_motion(self, event, pos):
        for comp in self.components:
            comp._on_mouse_motion(pos)

    def on_mouse_down(self, event, pos):
        return
