import pygame

from src import config
from .component import Component
from ..elements import *


class Header(Component):

    def __init__(self, x, y, w, h, background, textbox):
        super().__init__(x, y, w, h)

        self.background = background
        self.textbox = textbox

    def on_update(self, elapsed):
        pass

    def _on_render(self, screen):
        self.background.on_render(screen)
        self.textbox.on_render(screen)

    @staticmethod
    def create_rectangle_header(x, y, w, h, back_color, text, text_col, text_size):
        background = Rectangle(0, 0, w, h, back_color)
        textbox = Textbox(0, 0, w, h, text, text_col, text_size)
        header = Header(x, y, w, h, background, textbox)

        return header
