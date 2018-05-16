
import pygame

from ..uielement import UIElement


class Image(UIElement):

    def __init__(self, x, y, w, h, file_name):
        super().__init__(x, y, w, h)

        self.file_name = file_name
        self.img_surf = pygame.transform.smoothscale(pygame.image.load(file_name), (self.w, self.h))

    def on_render(self, screen, animation_progress=0):
        screen.blit(self.img_surf, self.get_pos())

    def on_update(self, elapsed):
        pass

    def on_mouse_down(self, pos):
        pass

    def on_mouse_up(self, pos):
        pass

    def on_mouse_motion(self, pos):
        pass
