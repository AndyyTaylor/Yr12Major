
import pygame
from ..ui.UIElement import UIElement
from .. import config


class Connection(UIElement):

    def __init__(self, in_holder, out_holder):
        self.in_holder = in_holder
        self.out_holder = out_holder

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        pygame.draw.line(screen, config.GREEN, self.in_holder.get_center(), self.out_holder.get_center(), 5)

    def on_mouse_motion(self, pos):
        pass

    def on_mouse_down(self, pos):
        pass

    def on_mouse_up(self, pos):
        pass
