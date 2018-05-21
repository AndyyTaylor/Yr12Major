
import pygame
import numpy as np

from src import config
from ..components import *
from ..elements import Textbox
from src.framework.StateRegistry import StateRegistry


class Screen():  # Screen (1) -> Components (3-4) -> Elements -> (5 each) -> Primitives (2-3 each)

    def __init__(self, name, parent, back_color=config.SCHEME5):
        self.name = name
        self.back_color = back_color  # default back color for screen
        self.parent = StateRegistry.instance().register(self, parent)

        # Will contain all screen components ~3-4
        self.components = []

    def on_init(self):
        " Called when the application is run "
        return

    def on_shutdown(self):
        " Called when the application is closed "
        return

    def on_enter(self, data, screen):
        pygame.draw.rect(screen, self.back_color, screen.get_rect())

        # Every component must initially render
        for comp in self.components:
            comp.changed = True

    def on_exit(self):
        " Called when the state is exited "
        return

    def on_update(self, elapsed):
        for comp in self.components:
            comp.on_update(elapsed)

    def on_render(self, screen):
        changed_rectangles = []
        for comp in self.components:
            if comp.has_changed():
                # (back color defaults to screen back color, rectangle to draw)
                changed_rectangles.append((comp.back_color or self.back_color
                                         , comp.get_prev_rect()))

        for rect in changed_rectangles:
            pygame.draw.rect(screen, *rect)

        for comp in self.components:
            if comp.has_changed():
                comp.on_render(screen)

    def on_key_down(self, key):
        return

    def on_mouse_event(self, event):
        return

    def on_mouse_motion(self, event, pos):
        for comp in self.components:
            comp.on_mouse_motion(pos)

    # This has to be handled here to prevent clicking multiple elements at once
    def on_mouse_down(self, event, pos):
        for comp in reversed(self.components):  # Reversed to respect depth properly
            if isinstance(comp, Button) and pygame.Rect(comp.get_rect()).collidepoint(pos):
                comp.on_click()
                return
