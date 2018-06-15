
import pygame
from src.framework import UIElement


class Widget(UIElement):

    def __init__(self, x, y, w, h, back_color, type, clickable=False):
        super().__init__(x, y, w, h)

        self.back_color = back_color
        self.type = type
        self.clickable = clickable

        self.changed = True
        self.is_clicked = False

    def reset_animation(self):
        self.animation = 0
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
        # temp = self.changed
        # self.changed = False
        #
        # return temp

        return self.changed
