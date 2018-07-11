
import pygame

from .widget import Widget


class Image(Widget):

    def __init__(self, x, y, w, h, file_name):
        super().__init__(x, y, w, h, None, "image")

        self.file_name = file_name
        self.img_surf = pygame.transform.smoothscale(pygame.image.load("data/assets/" + file_name),
                                                     (self.w, self.h))

    def on_init(self):
        return

    def on_shutdown(self):
        return

    def on_enter(self, data, screen):
        return

    def on_exit(self):
        return

    def on_update(self, elapsed):
        return

    def on_render(self, screen, back_fill=None):
        screen.blit(self.img_surf, self.get_pos())

        self.changed = False
