import pygame

from src import config
from .component import Component
from ..elements import *
from ..primitives import *


class Header(Component):

    def __init__(self, x, y, w, h, screen, background, textbox):
        super().__init__(x, y, w, h, screen)

        self.background = background
        self.textbox = textbox

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.background.render(screen)
        self.textbox.render(screen)

    @staticmethod
    def create_rectangle_header(x, y, w, h, back_color, text, text_col, text_size, screen):
        background = Rectangle(0, 0, w, h, back_color)
        textbox = Textbox(0, 0, w, h, text, text_col, text_size)
        header = Header(x, y, w, h, screen, background, textbox)

        return header
