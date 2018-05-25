
import pygame, random
import numpy as np
from ..basicelement import BasicElement
from ..elements import Button


class Component(BasicElement):

    def __init__(self, x, y, w, h, screen, scrollable=False, back_color=None):
        super().__init__(x, y, w, h)
        self.scrollable = scrollable
        self.back_color = back_color
        self.screen = screen

        self.x_shift = 0
        self.y_shift = 0

        self.elements = []

        self.prev_rect = self.get_rect()

    def on_render(self, data, surf):
        if back_color is not None:
            surf.fill(self.back_color)

        for elem in self.elements:
            elem.changed = True

    def on_update(self, elapsed):
        self.update(elapsed)

        #  print(int(1000 / elapsed))

    def on_render(self, screen, **kwargs):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        if self.x_shift != 0 or self.y_shift != 0:
            max_width = surf.get_width() + abs(self.x_shift)
            max_heigth = surf.get_height() + abs(self.y_shift)
            temp_surf = pygame.Surface((max_width, max_height))

            self.render(temp_surf)
            surf.blit(temp_surf, (self.x_shift, self.y_shift))
        else:
            print('RENDERING:', random.randint(0, 10), self.changed)
            self.render(surf)

        screen.blit(surf, (self.x, self.y))
        self.prev_rect = self.get_rect()
        self.changed = False

    def on_scroll_wheel(self, direction):
        if self.scrollable:
            self.y_shift += 40 * direction

    def get_prev_rect(self):
        return self.prev_rect

    def on_mouse_motion(self, pos):
        for elem in self.elements:
            elem.on_mouse_motion(pos)

    def on_mouse_down(self, pos):
        for elem in reversed(self.elements):  # Reversed to respect depth properly
            if isinstance(elem, Button) and pygame.Rect(elem.get_rect()).collidepoint(pos):
                elem.on_click()
                return
