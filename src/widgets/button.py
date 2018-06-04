
import pygame, datetime
import numpy as np

from src import config
from .widget import Widget
from src.framework.StateRegistry import StateRegistry
from src.framework import UIElement


class Shape(UIElement):

    def __init__(self, x, y, w, h, color, alpha_enabled=False):
        super().__init__(x, y, w, h)

        self.color = color
        self.alpha_enabled = alpha_enabled

    def render(self, screen, x_off, y_off, animation=0):
        return


class Rect(Shape):

    def render(self, screen, x_off, y_off, animation=0):
        rect = self.get_rect()
        adj_rect = (rect[0] + x_off, rect[1] + y_off, rect[2], rect[3])

        pygame.draw.rect(screen, self.color, adj_rect)


class RoundedRect(Shape):

    def __init__(self, x, y, w, h, color, alpha_enabled=False):
        super().__init__(x, y, w, h, color, alpha_enabled)

        self.cache = []
        self.prev_animation = 0

    def render(self, screen, x_off, y_off, animation=0):
        rect = self.get_rect()
        adj_rect = (rect[0] + x_off, rect[1] + y_off, rect[2], rect[3])

        if animation != self.prev_animation:
            self.cache = []
            self.prev_animation = animation

        if self.alpha_enabled:
            self.draw_rounded_rect(screen, adj_rect, (*self.color, int(animation*50)), 0.4+animation*0.6)
        else:
            self.draw_rounded_rect(screen, adj_rect, self.color, 0.4+animation*0.6)

    def draw_rounded_rect(self, surface, rect, color, radius=0.4):
        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """
        pos = (rect[0], rect[1])

        if not self.cache:
            rect = pygame.Rect(rect)
            color = pygame.Color(*color)
            alpha = color.a
            color.a = 0
            pos = rect.topleft
            rect.topleft = 0, 0
            rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

            circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
            pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
            circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

            radius = rectangle.blit(circle, (0, 0))
            radius.bottomright = rect.bottomright
            rectangle.blit(circle, radius)
            radius.topright = rect.topright
            rectangle.blit(circle, radius)
            radius.bottomleft = rect.bottomleft
            rectangle.blit(circle, radius)

            rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
            rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

            rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
            rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

            self.cache.append(rectangle)

        return surface.blit(self.cache[0], pos)


class Button(Widget):

    def __init__(self, x, y, w, h, text, font_size, font_col, back_color, front_color, border_width, callback, shape='rounded_rect'):
        super().__init__(x, y, w, h, back_color, "label")

        self.back_color = back_color
        self.front_color = front_color
        self.border_width = border_width

        self.text = text
        self.font_size = font_size
        self.font_col = font_col

        self.callback = callback

        self.font = pygame.font.Font('%s/data/fonts/%s' % (config.DIR_PATH, 'Square.ttf'), self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.font_col)

        self.shapes = []

        if shape == 'rounded_rect':
            ShapeClass = RoundedRect
        elif shape == 'rect':
            ShapeClass = Rect
        else:
            raise NotImplementedError("Can't find shape " + shape)

        self.shapes.append(ShapeClass(0, 0, w, h, self.back_color))
        self.shapes.append(ShapeClass(border_width, border_width, w - 2*border_width, h - 2*border_width, self.front_color))

        self.alpha_cover = ShapeClass(0, 0, w, h, config.WHITE, True)

        self.prev_hash = None
        self.animation = 0
        self.animation_time = 150
        self.hover = False

    def on_update(self, elapsed):
        if self.hover and self.animation < self.animation_time:
            dt = min(elapsed, self.animation_time - self.animation)
            self.animation += dt
        elif not self.hover and self.animation > 0:
            dt = min(elapsed, self.animation)
            self.animation -= dt

        new_hash = hash((self.hover, self.animation))

        if new_hash != self.prev_hash:
            self.changed = True
            self.prev_hash = new_hash

    def on_render(self, screen, back_fill=None):
        if back_fill is not None:
            pygame.draw.rect(screen, back_fill, self.get_rect())

        for shape in self.shapes:
            shape.render(screen, self.x, self.y, self.animation / self.animation_time)

        t_w, t_h = self.font.size(self.text)
        screen.blit(self.rendered_text, self.get_adj_center(t_w / 2, t_h / 2))

        self.alpha_cover.render(screen, self.x, self.y, self.animation / self.animation_time)

    def on_mouse_motion(self, pos):
        self.hover = pygame.Rect(self.get_rect()).collidepoint(pos)

    def on_click(self, pos):
        self.callback()
