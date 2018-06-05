
import pygame
import numpy as np

from src import config
from .widget import Widget


class Frame(Widget):

    def __init__(self, x, y, w, h, scrollable=False, back_color=None, **kwargs):
        super().__init__(x, y, w, h, None, 'frame')

        self.scrollable = scrollable
        self.scroll_y = 0
        self.scroll_x = 0
        self.min_scroll_y = 0
        self.max_scroll_y = 500
        self.max_scroll_x = 0

        # defaults = {
        #     'min_scroll_y': 0,
        #     'max_scroll_y': 500,
        #     'min_scroll_x': 0,
        #     'max_scroll_x': 500
        # }

        self.children = []
        self.prev_hash = None
        self.back_color = back_color

        self.surf = pygame.Surface((self.w + 2 * self.max_scroll_x, self.h + 2 * self.max_scroll_y))
        self.has_filled = False

    def on_update(self, elapsed):
        for child in self.children:
            child.on_update(elapsed)

        new_hash = hash((self.scroll_x, self.scroll_y))
        if new_hash != self.prev_hash:
            self.prev_hash = new_hash
            self.changed = True

    def on_render(self, screen, back_fill=None):
        if self.back_color is not None:
            back_fill = self.back_color

        if not self.has_filled and back_fill is not None:
            self.surf.fill(back_fill)
            self.has_filled = True

        for child in self.children:  # Crop things that are out of the Frame
            if child.has_changed():
                child.on_render(self.surf, back_fill)

        temp_surf = pygame.Surface((self.w, self.h))
        if back_fill is not None:
            temp_surf.fill(back_fill)
        temp_surf.blit(self.surf, (self.scroll_x, self.scroll_y))

        screen.blit(temp_surf, (self.x, self.y))

    def on_mouse_motion(self, pos):
        for child in self.children:
            child.on_mouse_motion(self.adj_pos(pos))

    def on_mouse_down(self, pos):
        pos = self.adj_pos(pos)
        for child in self.children:
            if pygame.Rect(child.get_rect()).collidepoint(pos):
                child.on_click(pos)

    def adj_pos(self, pos):
        return np.subtract(np.subtract(pos, (self.x, self.y)), (self.scroll_x, self.scroll_y))

    def add_child(self, child):
        self.children.append(child)

    def on_scroll(self, is_down):
        if not self.scrollable:
            return

        if is_down:
            self.scroll_y -= config.SCROLL_SPEED
        else:
            self.scroll_y += config.SCROLL_SPEED

        self.scroll_y = self.crop(self.scroll_y, -self.max_scroll_y, 0)

    def crop(self, val, min_val, max_val):
        return max(min(val, max_val), min_val)

    def has_changed(self):
        for child in self.children:
            if child.has_changed():
                return True

        return self.changed
