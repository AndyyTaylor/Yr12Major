
import pygame
import numpy as np

from src.framework import UIElement


class Widget(UIElement):

    def __init__(self, x, y, w, h, back_color, type, clickable=False, parent=None):
        super().__init__(x, y, w, h)

        self.back_color = back_color
        self.type = type
        self.clickable = clickable
        self.parent = parent

        self.changed = True
        self.is_clicked = False
        self.was_clicked = False

    def reset_animation(self):
        self.animation = 0
        self.hover = False
        self.is_clicked = False

    def on_init(self):
        return

    def on_shutdown(self):
        return

    def on_enter(self, data, screen):
        return

    def on_exit(self):
        return

    def on_update(self, elapsed):
        self.update_prev_pos()

    def on_render(self, screen, back_fill=None):
        if back_fill is not None:
            pygame.draw.rect(screen, back_fill, self.get_prev_rect())

    def on_key_down(self, key):
        return

    def on_mouse_event(self, event):
        return

    def on_mouse_motion(self, pos):
        # if pygame.Rect(self.get_rect()).collidepoint(pos):  # This could slow fps a bit
        #     self.changed = True
        return

    def on_mouse_down(self, pos):
        return

    def on_mouse_up(self, pos):
        self.is_clicked = False

    def on_click(self, pos):
        if self.clickable:
            self.is_clicked = True
            return True

        return False

    def on_scroll(self, is_down):
        return

    def has_changed(self):
        return self.changed

    def get_global_pos(self, cast=False):
        if self.parent is None:
            return self.get_pos(cast)

        pos = tuple(np.add(self.parent.get_global_pos(cast), self.get_pos(cast)))
        if self.parent.type == 'frame':  # and not self.float
            pos = np.add(pos, self.parent.get_scroll())

        return pos

    def get_global_center(self, cast=False):
        if cast:
            return tuple(np.add(self.get_global_pos(True), (int(self.w / 2), int(self.h / 2))))
        else:
            return tuple(np.add(self.get_global_pos(), (self.w / 2, self.h / 2)))

    def get_global_rect(self):
        return self.get_global_pos() + (self.w, self.h)
