import pygame

from .. import config
from .UIElement import UIElement


class RoundedButton(UIElement):

    def __init__(self, x, y, w, h, border, back_col, front_col, callback):
        super().__init__(x, y, w, h)
        self.border = border
        self.back_col = back_col
        self.front_col = front_col
        self.callback = callback

        self.hover = False
        self.hover_time = 0
        self.hover_alpha = 0
        self.max_hover_alpha = 100

        self.animation_speed = 150

        self.rectangle = None
        self.prev_hash = None

        self.enabled = True

        self.cache = []

    def on_update(self, elapsed):
        if not self.enabled:
            return

        if self.hover and self.hover_time < self.animation_speed:
            dt = min(elapsed, self.animation_speed - self.hover_time)
            self.hover_alpha += dt / self.animation_speed * self.max_hover_alpha
            self.hover_time += dt
        elif not self.hover and self.hover_time > 0:
            dt = min(elapsed, self.hover_time)
            self.hover_alpha -= dt / self.animation_speed * self.max_hover_alpha
            self.hover_time -= dt

    def on_render(self, screen):
        new_hash = hash((self.hover_alpha, self.enabled))
        if new_hash != self.prev_hash:
            self.cache = []

        self.draw_rounded_rect(screen, (self.x, self.y, self.w, self.h), self.back_col, 0, 0.4 + 0.6 * (self.hover_time / self.animation_speed))
        self.draw_rounded_rect(screen, (self.x+self.border, self.y+self.border, self.w-self.border*2, self.h-self.border*2), self.front_col, 1, 0.4 + 0.6 * (self.hover_time / self.animation_speed))

        if self.enabled:
            self.draw_rounded_rect(screen, (self.x, self.y, self.w, self.h), (*config.WHITE, int(self.hover_alpha)), 2, 0.4 + 0.6 * (self.hover_time / self.animation_speed))
        else:
            self.draw_rounded_rect(screen, (self.x, self.y, self.w, self.h), (*config.BLACK, 50), 2)

        self.prev_hash = new_hash

    def on_mouse_motion(self, pos):
        self.hover = pygame.Rect(self.x, self.y, self.w, self.h).collidepoint(pos)

    def on_mouse_up(self, pos):
        pass

    def on_mouse_down(self, pos):
        if pygame.Rect(self.get_rect()).collidepoint(pos):
            self.on_click()

    def reset_animation(self):
        self.hover_time = 0

    def on_click(self):
        if self.enabled:
            self.callback()

    def disable(self):
        self.enabled = False

    def draw_rounded_rect(self, surface, rect, color, cache_ind, radius=0.4):
        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """
        pos = (rect[0], rect[1])

        if len(self.cache) <= cache_ind:
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

        return surface.blit(self.cache[cache_ind], pos)
