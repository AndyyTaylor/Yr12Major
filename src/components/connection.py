
import pygame

from src import config
from src.framework import UIElement


class Connection(UIElement):

    def __init__(self, in_holder, out_holder):
        self.in_holder = in_holder
        self.out_holder = out_holder

        self.data = []

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)
