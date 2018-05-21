import pygame

from src import config
from ..basicelement import BasicElement


class RoundedRect(BasicElement):

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color

        self.max_hover_alpha = 100
        self.animation_speed = 150

        self.rectangle = None
        self.prev_hash = None

        self.enabled = True

        self.cache = []

    def on_render(self, screen, animation_progress=0):
        new_hash = hash((animation_progress))
        if new_hash != self.prev_hash:
            self.cache = []

        self.draw_rounded_rect(screen, (self.x, self.y, self.w, self.h), self.color, 0, 0.4 + 0.6 * animation_progress)

        self.prev_hash = new_hash

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
