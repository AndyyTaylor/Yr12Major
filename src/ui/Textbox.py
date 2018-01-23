import pygame

from .. import config
from .UIElement import UIElement

class Textbox(UIElement):
    def __init__(self, x, y, w, h, text, text_col, size):  # pylint: disable=R0913
        super().__init__(x, y, w, h)

        self.text = text
        self.text_col = text_col

        self.font = pygame.font.Font('%s/data/fonts/%s' % (config.dir_path, 'Square.ttf'), size)
        self.rendered_text = self.font.render(self.text, True, self.text_col)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        t_w, t_h = self.font.size(self.text)
        screen.blit(self.rendered_text, self.get_adj_center(t_w / 2, t_h / 2))
