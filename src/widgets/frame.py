
import pygame
import numpy as np

from src import config
from .widget import Widget
from src.framework.StateRegistry import StateRegistry


class Frame(Widget):

    def __init__(self, x, y, w, h, scrollable=False):
        super().__init__(x, y, w, h, None, 'frame')

        self.children = []

    def on_update(self, elapsed):
        for child in self.children:
            child.on_update(elapsed)

    def on_render(self, screen, back_fill=None):
        for child in self.children:
            if child.has_changed():
                child.on_render(screen, back_fill)

    def on_mouse_motion(self, pos):
        for child in self.children:
            child.on_mouse_motion(pos)

    def add_child(self, child):
        self.children.append(child)

    def has_changed(self):
        for child in self.children:
            if child.has_changed():
                return True

        return False
