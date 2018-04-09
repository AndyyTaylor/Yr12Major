" Andy "
import pygame

from .. import config
from ..ui import RoundedButton
from ..ui import Textbox
from .AbstractState import State


class LevelSelector(State):
    " A "

    def __init__(self):
        super().__init__("LevelSelector", "MasterState")

        self.x_margin = 50
        self.y_margin = 120

        self.box_width = 150
        self.box_height = self.box_width
        self.box_border = 10

        num_boxes_per_row = 6
        self.gap_size = int(((config.SCREEN_WIDTH - self.x_margin*2) - num_boxes_per_row * self.box_width) / (num_boxes_per_row-1))

        self.elements = []

        level_num = 1
        for yy in range(self.y_margin, config.SCREEN_HEIGHT, self.box_height + self.gap_size):
            for xx in range(self.x_margin, config.SCREEN_WIDTH - self.x_margin, self.box_width + self.gap_size):
                self.create_level_button(xx, yy, level_num)
                level_num += 1

    def on_update(self, elapsed):
        for element in self.elements:
            element.on_update(elapsed)

    def on_render(self, screen):
        screen.fill(config.SCHEME5)

        for element in self.elements:
            element.on_render(screen)

    def on_mouse_down(self, event, pos):
        for element in self.elements:
            if isinstance(element, RoundedButton) and pygame.Rect(element.get_rect()).collidepoint(pos):
                element.on_click()
                return

    def on_mouse_up(self, event, pos):
        return  # TODO proper clicking

    def on_mouse_motion(self, event, pos):
        for element in self.elements:
            element.on_mouse_motion(pos)

    def create_level_button(self, x, y, level_num):
        button = RoundedButton(x, y, self.box_width, self.box_height, self.box_border, config.SCHEME4, config.SCHEME3, lambda: self.parent.change_state("Level", level_num))
        if level_num > config.MAX_LEVEL:
            button.disable()

        self.elements.append(button)
        self.elements.append(Textbox(x, y, self.box_width, self.box_height, str(level_num), config.SCHEME1, 72))
