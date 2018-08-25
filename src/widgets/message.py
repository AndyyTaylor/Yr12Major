
import pygame

from src import config
from .widget import Widget


class Message(Widget):

    def __init__(self, x, y, w, h, back_color, text, font_size, font_col, align='cc'):
        super().__init__(x, y, w, h, back_color, "message")

        self.text = text
        self.font_size = font_size
        self.font_col = font_col
        self.align = align

        self.font = pygame.font.Font('data/fonts/%s' % ('Square.ttf'),
                                     self.font_size)
        self.render_text()

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

    def change_text(self, text):
        text = str(text)
        if text == self.text:
            return

        self.text = text
        self.changed = True
        self.render_text()

    def change_color(self, color):
        if color == self.font_col:
            return

        self.font_col = color
        self.changed = True
        self.render_text()

    def render_text(self):
        self.rendered_text = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        words = self.text.split() + ['zzz']
        sentence = ''
        current_height = 0
        for word in words:
            t_w, t_h = self.font.size(sentence + word + ' ')

            if t_w > self.w or word == 'zzz' or word == '<new>':
                t_render = self.font.render(sentence, True, self.font_col)
                self.rendered_text.blit(t_render, (0, current_height))
                sentence = ''
                current_height += t_h

            if word != '<new>':
                sentence += word + ' '

    def on_render(self, screen, back_fill=None):
        if self.back_color is None:
            back_fill = None

        super().on_render(screen, back_fill)

        if self.back_color is not None:
            pygame.draw.rect(screen, self.back_color, self.get_rect())
        elif back_fill is not None:
            pygame.draw.rect(screen, back_fill, self.get_rect())

        if self.align[0] == 'c':
            t_w, t_h = self.font.size(self.text)
            x = self.get_adj_center(t_w / 2, t_h / 2)[0]
        elif self.align[0] == 'l':
            x = self.get_pos()[0]

        if self.align[1] == 'c':
            t_w, t_h = self.font.size(self.text)
            y = self.get_adj_center(t_w / 2, t_h / 2)[1]
        elif self.align[1] == 'l':
            y = self.get_pos()[1]

        screen.blit(self.rendered_text, (x, y))

        self.changed = False
