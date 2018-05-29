
import pygame
import numpy as np

from src import config
from ..widgets import *
from src.framework.StateRegistry import StateRegistry


class Screen():

    def __init__(self, name, parent, back_color=config.SCHEME5):
        self.name = name
        self.back_color = back_color
        self.parent = StateRegistry.instance().register(self, parent)

        self.widgets = []

    def on_init(self):
        for widget in self.widgets:
            widget.on_init()

    def on_shutdown(self):
        for widget in self.widgets:
            widget.on_shutdown()

    def on_enter(self, data, screen):
        pygame.draw.rect(screen, self.back_color, screen.get_rect())

        for widget in self.widgets:
            widget.on_render(screen)

    def on_exit(self):
        for widget in self.widgets:
            widget.on_exit()

    def on_update(self, elapsed):
        for widget in self.widgets:
            widget.on_update(elapsed)

    def on_render(self, screen):
        for widget in self.widgets:
            if widget.has_changed():
                widget.on_render(screen, self.back_color)

    def on_key_down(self, key):
        for widget in self.widgets:
            widget.on_key_down(key)

    def on_mouse_event(self, event):
        for widget in self.widgets:
            widget.on_mouse_event(event)

    def on_mouse_motion(self, event, pos):
        for widget in self.widgets:
            widget.on_mouse_motion(pos)

    def on_mouse_down(self, event, pos):
        for widget in self.widgets:
            widget.on_mouse_down(pos)

    def on_mouse_up(self, event, pos):
        for widget in self.widgets:
            widget.on_mouse_up(pos)
