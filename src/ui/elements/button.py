import pygame

from src import config
from ..basicelement import BasicElement
from ..primitives import *
from .textbox import Textbox


class Button(BasicElement):

    def __init__(self, x, y, w, h, back_shape, front_shape, textbox, callback):
        super().__init__(x, y, w, h)
        self.back_shape = back_shape
        self.front_shape = front_shape
        self.textbox = textbox
        self.callback = callback

        self.primitives = [
            back_shape,
            front_shape,
            textbox
        ]
        self.disabled_cover = RoundedRect(*back_shape.get_rect(), config.BLACK)

        self.hover = False
        self.hover_time = 0
        self.hover_alpha = 0

        self.animation_speed = 150
        self.max_hover_alpha = 100

        self.enabled = True

        self.prev_hash = None

    def update(self, elapsed):
        if not self.enabled:
            return

        if self.hover and self.hover_time < self.animation_speed:
            dt = min(elapsed, self.animation_speed - self.hover_time)
            self.hover_time += dt
        elif not self.hover and self.hover_time > 0:
            dt = min(elapsed, self.hover_time)
            self.hover_time -= dt

        new_hash = hash((self.hover_time, self.enabled))
        if new_hash != self.prev_hash:
            self.changed = True
            self.prev_hash = new_hash

    def render(self, screen):
        animation_progress = self.hover_time / self.animation_speed

        for primitive in self.primitives:
            primitive.on_render(screen, animation_progress=animation_progress)

        if not self.enabled:
            s = pygame.Surface(self.disabled_cover.get_size())
            s.set_alpha(128)
            self.disabled_cover.on_render(s)
            screen.blit(s, self.get_pos())

        self.changed = False

    def on_mouse_motion(self, pos):
        self.hover = pygame.Rect(self.get_rect()).collidepoint(pos)

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

    @staticmethod
    def create_rounded_button(x, y, w, h, back_col, front_col, border_width, text, text_col, text_size, callback):
        back_shape = RoundedRect(x, y, w, h, back_col)
        front_shape = RoundedRect(x + border_width, y + border_width, w - border_width*2, h - border_width*2, front_col)
        textbox = Textbox(x, y, w, h, text, text_col, text_size)

        return Button(x, y, w, h, back_shape, front_shape, textbox, callback)

    @staticmethod
    def create_rounded_image_button(x, y, w, h, back_col, front_col, border_width, img_x, img_y, img_w, img_h, file_name, callback):
        back_shape = RoundedRect(x, y, w, h, back_col)
        front_shape = RoundedRect(x + border_width, y + border_width, w - border_width*2, h - border_width*2, front_col)
        image = Image(img_x - x, img_y - y, img_w, img_h, file_name)

        return Button(x, y, w, h, back_shape, front_shape, image, callback)
