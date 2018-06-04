
import pygame
import numpy as np

from src import config
from src.framework.StateRegistry import StateRegistry
from src.framework import UIElement


class Widget(UIElement):

    def __init__(self, x, y, w, h, back_color, type):
        super().__init__(x, y, w, h)

        self.back_color = back_color
        self.type = type

        self.changed = True

    def on_init(self):
        return

    def on_shutdown(self):
        return

    def on_enter(self, data, screen):
        return

    def on_exit(self):
        return

    def on_update(self, elapsed):
        return

    def on_render(self, screen, back_fill=None):
        return

    def on_key_down(self, key):
        return

    def on_mouse_event(self, event):
        return

    def on_mouse_motion(self, pos):
        return

    def on_mouse_down(self, pos):
        return

    def on_mouse_up(self, pos):
        return

    def on_click(self, pos):
        return

    def has_changed(self):
        # temp = self.changed
        # self.changed = False
        #
        # return temp

        return self.changed
