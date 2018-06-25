import pygame

from .. import config
from .UIElement import UIElement


class Button(UIElement):
    def __init__(self, x, y, w, h, back_col, front_col, text, text_col, font_size, callback):   # pylint: disable=R0913
        super().__init__(x, y, w, h)

        self.callback = callback
        self.back_col = back_col
        self.front_col = front_col
        self.border_width = 10
        self.text = text
        self.text_col = text_col

        self.font = pygame.font.Font('%s/data/fonts/%s' % (config.DIR_PATH, 'Square.ttf'), font_size)
        self.rendered_text = self.font.render(self.text, True, self.text_col)

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        pygame.draw.rect(screen, self.back_col, self.get_rect())
        pygame.draw.rect(screen, self.front_col, (
            self.x + self.border_width, self.y + self.border_width,
            self.w - self.border_width * 2, self.h - self.border_width * 2))

        t_w, t_h = self.font.size(self.text)
        screen.blit(self.rendered_text, self.get_adj_center(t_w / 2, t_h / 2))

    def on_click(self):
        self.callback()
