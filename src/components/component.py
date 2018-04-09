
import pygame
from ..ui.UIElement import UIElement


class Component(UIElement):

    def __init__(self, x, y, w, h, draggable=True):
        super().__init__(x, y, w, h)

        self.draggable = draggable
        self.clicked = False

        self.slot_width = 40
        self.slot_height = 30

        self.mouse_offset_x = None
        self.mouse_offset_y = None

        self.text = None

    def on_update(self, elapsed):
        return

    def on_render(self, screen):
        return

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.text.x = x
        self.text.y = y

    def on_mouse_down(self, pos):
        if pygame.Rect(self.get_rect()).collidepoint(pos):
            self.clicked = True
            self.mouse_offset_x = pos[0] - self.x
            self.mouse_offset_y = pos[1] - self.y

    def on_mouse_up(self, pos):
        self.clicked = False

    def on_mouse_motion(self, pos):
        if self.clicked:
            self.set_pos(pos[0] - self.mouse_offset_x, pos[1] - self.mouse_offset_y)

    def draw_rounded_rect(self, surface, rect, color, radius=0.1):
        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """
        pos = (rect[0], rect[1])

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

        return surface.blit(rectangle, pos)
