" Andy "
import pygame

from src import config
# from ..elements import Textbox
# from ..components import Button
from ..components import *
from .screen import Screen


class LevelSelector(Screen):
    " A "

    def __init__(self):
        super().__init__("LevelSelector", "MasterState")

        self.x_margin = 50
        self.y_margin = 150

        self.box_width = 150
        self.box_height = self.box_width
        self.box_border = 10

        num_boxes_per_row = 6
        self.gap_size = int(((config.SCREEN_WIDTH - self.x_margin*2) - num_boxes_per_row * self.box_width) / (num_boxes_per_row-1))

        self.components = []

        self.past_level = config.MAX_LEVEL
        self.create_level_buttons()
        self.create_title()

    def on_enter(self, data, screen):
        super().on_enter(data, screen)
        # pygame.draw.rect(screen, config.SCHEME2, (0, 200, config.SCREEN_WIDTH, 100))
        if self.past_level != config.MAX_LEVEL:
            self.past_level = config.MAX_LEVEL

            self.components = []
            self.create_level_buttons()
            self.create_title()
        else:
            for comp in self.components:
                comp.reset_animation()

    def on_update(self, elapsed):
        super().on_update(elapsed)

    def on_render(self, screen):
        super().on_render(screen)

    def on_mouse_down(self, event, pos):
        for comp in self.components:
            if isinstance(comp, Button) and pygame.Rect(comp.get_rect()).collidepoint(pos):
                comp.on_click()
                return

    def on_mouse_up(self, event, pos):
        for comp in self.components:
            comp.on_mouse_up(pos)

    def create_title(self):
        self.components.append(Header.create_rectangle_header(
                                0, 0, config.SCREEN_WIDTH, 100, config.SCHEME2,
                                "Level Selection", config.BLACK, 72, self)
                              )

    def create_level_buttons(self):
        self.components.append(LevelButtons(self.x_margin, self.y_margin, config.SCREEN_WIDTH - self.x_margin * 2, config.SCREEN_HEIGHT - self.y_margin * 2, self, self.box_width, self.box_height, self.gap_size, 3))
