
from src import config
from .screen import Screen
from ..widgets import Frame, Button


class LevelSelector(Screen):

    def __init__(self):
        super().__init__('LevelSelector', 'MasterState', back_screen='MainMenu')

        self.create_level_buttons(50, 170, config.SCREEN_WIDTH - 100,
                                  config.SCREEN_HEIGHT + 200, 150, 150, 20)
        self.max_level = config.MAX_LEVEL

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if config.MAX_LEVEL != self.max_level:
            for button in self.level_button_frame.children:
                if int(button.text) <= config.MAX_LEVEL:
                    button.enable()
                else:
                    button.disable()

            self.max_level = config.MAX_LEVEL

    def create_level_buttons(self, x, y, w, h, box_width, box_height, gap_size):
        level_button_frame = Frame(x, y, w, h, True, config.SCHEME5,
                                   min_scroll_y=-500, max_scroll_y=0)
        self.widgets.append(level_button_frame)
        self.level_button_frame = level_button_frame

        level_num = 1
        for yy in range(y, y + h - box_height + 1, box_height + gap_size):
            for xx in range(x, x + w - box_width + 1, box_width + gap_size):
                button = self.create_level_button(xx - x, yy - y, level_num, box_width, box_height)
                level_button_frame.add_child(button)
                level_num += 1

    def create_level_button(self, x, y, level_num, box_width, box_height):
        button = Button(x, y, box_width, box_height, str(level_num),
                        72, config.BLACK, config.SCHEME4, config.SCHEME3, 10,
                        lambda: self.parent.change_state("Level", level_num))

        if level_num > config.MAX_LEVEL:
            button.disable()

        return button
