
import pygame

from src import config
from .widget import Widget


class Label(Widget):

    def __init__(self, x, y, w, h, back_color, text, font_size, font_col):
        super().__init__(x, y, w, h, back_color, "label")

        self.text = text
        self.font_size = font_size
        self.font_col = font_col

        self.font = pygame.font.Font('%s/data/fonts/%s' % (config.DIR_PATH, 'Square.ttf'),
                                     self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.font_col)

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
        pygame.draw.rect(screen, self.back_color, self.get_rect())

        t_w, t_h = self.font.size(self.text)
        screen.blit(self.rendered_text, self.get_adj_center(t_w / 2, t_h / 2))

        self.changed = False
