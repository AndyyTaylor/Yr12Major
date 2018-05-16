
import pygame
from ..uielement import UIElement


class Component(UIElement):

    def __init__(self, x, y, w, h, scrollable=False):
        super().__init__(x, y, w, h)
        self.scrollable = scrollable

        self.x_shift = 0
        self.y_shift = 0

        self.prev_rect = self.get_rect()

    def on_render(self, screen, **kwargs):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        if self.x_shift != 0 or self.y_shift != 0:
            max_width = surf.get_width() + abs(self.x_shift)
            max_heigth = surf.get_height() + abs(self.y_shift)
            temp_surf = pygame.Surface((max_width, max_height))

            self._on_render(temp_surf)
            surf.blit(temp_surf, (self.x_shift, self.y_shift))
        else:
            self._on_render(surf)

        screen.blit(surf, (self.x, self.y))
        self.prev_rect = self.get_rect()
        self.changed = False

    def on_scroll_wheel(self, direction):
        if self.scrollable:
            self.y_shift += 40 * direction

    def get_prev_rect(self):
        return self.prev_rect

    def _on_mouse_motion(self, pos):
        return