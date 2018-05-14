import pygame

from src import config
from ..uielement import UIElement


class Textbox(UIElement):
    def __init__(self, x, y, w, h, text, text_col, size):  # pylint: disable=R0913
        super().__init__(x, y, w, h)

        self.text = text
        self.prev_text = text
        self.text_col = text_col

        self.font = pygame.font.Font('%s/data/fonts/%s' % (config.DIR_PATH, 'Square.ttf'), size)
        self.rendered_text = self.font.render(self.text, True, self.text_col)

    def on_update(self, elapsed):
        if self.text != self.prev_text:
            self.prev_text = self.text
            self.changed = True

    def on_render(self, screen, animation_progress=0):
        super().on_render(screen)

        t_w, t_h = self.font.size(self.text)
        screen.blit(self.rendered_text, self.get_adj_center(t_w / 2, t_h / 2))

    def set_text(self, val):
        self.text = str(val)

        self.rendered_text = self.font.render(self.text, True, self.text_col)

    def set_col(self, val):
        self.text_col = val

        self.rendered_text = self.font.render(self.text, True, self.text_col)

    def on_mouse_up(self, pos):
        pass

    def on_mouse_down(self, pos):
        pass
