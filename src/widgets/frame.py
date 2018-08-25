
import pygame
import numpy as np

from src import config
from .widget import Widget


class Frame(Widget):

    def __init__(self, x, y, w, h, scrollable=False, back_color=None, **kwargs):
        super().__init__(x, y, w, h, None, kwargs.get('name', 'frame'), clickable=True)

        self.scrollable = scrollable
        self.scroll_y = 0
        self.scroll_x = 0

        defaults = {
            'min_scroll_y': -500,
            'max_scroll_y': 0,
            'min_scroll_x': 0,
            'max_scroll_x': 500,
            'grid_type': 'default',
            'item_gap': 20,
            'item_x_margin': 10,
            'hidden': False
        }

        for key, val in defaults.items():
            setattr(self, key, kwargs.get(key, val))

        self.children = []
        self.prev_hash = None
        self.back_color = back_color

        self.surf = pygame.Surface((self.w + abs(self.min_scroll_x) + self.max_scroll_x,
                                    self.h + abs(self.min_scroll_y) + self.max_scroll_y))
        self.has_filled = False
        self.scrolled = False

    def on_update(self, elapsed):
        super().on_update(elapsed)

        for child in self.children:
            child.on_update(elapsed)

        new_hash = hash((self.scroll_x, self.scroll_y))
        if new_hash != self.prev_hash:
            self.prev_hash = new_hash
            self.scrolled = True

    def on_render(self, screen, back_fill=None):
        if not self.hidden:
            super().on_render(screen, back_fill)

            if self.back_color is not None:
                back_fill = self.back_color

            if (not self.has_filled or self.changed) and back_fill is not None:
                self.surf.fill(back_fill)
                self.has_filled = True

            for child in self.children:
                if child.has_changed():
                    for other_child in self.children:
                        if pygame.Rect(child.get_rect()).colliderect(
                            pygame.Rect(other_child.get_rect())
                        ):
                            other_child.changed = True

            for child in self.children:  # Crop things that are out of the Frame
                if child.has_changed() or self.changed:
                    child.on_render(self.surf, back_fill)

            temp_surf = pygame.Surface((self.w, self.h))
            if back_fill is not None:
                temp_surf.fill(back_fill)
            temp_surf.blit(self.surf, (self.scroll_x, self.scroll_y))

            screen.blit(temp_surf, (self.x, self.y))
        else:
            super().on_render(screen)

        self.changed = False
        self.scrolled = False

    def on_mouse_motion(self, pos):
        for child in self.children:
            child.on_mouse_motion(self.adj_pos(pos))

    def on_mouse_down(self, pos):
        pos = self.adj_pos(pos)
        for child in self.children:
            if child.type == 'component' or child.type == 'frame':
                if not child.on_mouse_down(pos):
                    if pygame.Rect(child.get_rect()).collidepoint(pos):
                        child.on_click(pos)
            elif pygame.Rect(child.get_rect()).collidepoint(pos):
                if child.on_click(pos):
                    return True

    def on_mouse_up(self, pos):
        super().on_mouse_up(pos)

        for child in self.children:
            child.on_mouse_up(pos)

    def adj_pos(self, pos):
        return np.subtract(np.subtract(pos, (self.x, self.y)), (self.scroll_x, self.scroll_y))

    def add_child(self, child):
        if self.grid_type == 'stack':
            self.stack_child(child)
        elif self.grid_type == 'grid':
            self.grid_child(child)
        else:
            child.x = self.crop(child.x, 0, self.w - child.w)
            child.y = self.crop(child.y, 0, self.h - child.h)

        child.parent = self
        self.children.append(child)

    def grid_child(self, child):
        locations = []
        for y in range(self.item_gap, self.h - self.min_scroll_y, child.h + self.item_gap):
            for x in range(self.item_x_margin, self.w - child.w, child.w + self.item_gap):
                locations.append((x, y))

        taken_locations = [c.get_pos() for c in self.children]

        for location in locations:
            if location not in taken_locations:
                child.x, child.y = location[0], location[1]

                return

        print("Couldn't fit item!")

    def stack_child(self, child):
        taken = [0]
        for widget in self.children:
            taken.append(widget.y)
            taken.append(widget.y + widget.h)

        taken.sort()
        min_gap = child.h + self.item_gap * 2

        child.y = None
        for i, val in enumerate(taken):
            if i % 2 != 0:
                continue

            if i >= len(taken) - 1:
                continue

            if taken[i + 1] - val >= min_gap:
                child.y = val + self.item_gap
                break

        if child.y is None:
            child.y = taken.pop() + self.item_gap
        child.x = self.item_x_margin

    def clear_children(self):
        self.children = []

    def on_scroll(self, is_down):
        if not self.scrollable:
            return

        if is_down:
            self.scroll_y -= config.SCROLL_SPEED
        else:
            self.scroll_y += config.SCROLL_SPEED

        self.scroll_y = self.crop(self.scroll_y, self.min_scroll_y, self.max_scroll_y)

    def crop(self, val, min_val, max_val):
        return max(min(val, max_val), min_val)

    def get_scroll(self):
        return (self.scroll_x, self.scroll_y)

    def has_changed(self):
        for child in self.children:
            if child.has_changed():
                return True

        return self.changed or self.scrolled

    def reset_animation(self):
        for child in self.children:
            child.reset_animation()

    def hide(self):
        self.hidden = True
        self.changed = True
