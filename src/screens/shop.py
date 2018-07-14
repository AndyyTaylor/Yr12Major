
import pygame
from src import config
from .screen import Screen
from ..widgets import Button, Frame


class Shop(Screen):

    def __init__(self):
        super().__init__("Shop", "MasterState")

        # I'm convinced I'm forgetting some stuff that will go on this screen

        shop_width = config.SCREEN_WIDTH

        self.shop_frame = Frame(0, 200, shop_width, config.SCREEN_HEIGHT - 200, True,
                                config.SCHEME5, gridded=True)
        self.widgets.append(self.shop_frame)

        # self.shop_frame.add_child(Button(0, 0, 300, 300, '', 0, config.BLACK, config.SCHEME3,
        #                                  config.SCHEME4, 10,
        #                                  lambda: print("Purchasing"), remould=False))
        self.shop_frame.add_child(Button(0, 0, 300, 300, '', 0, config.BLACK, config.SCHEME3,
                                         config.SCHEME4, 10,
                                         lambda: print("Purchasing"), remould=False))
        self.shop_frame.add_child(Button(0, 0, 300, 300, '', 0, config.BLACK, config.SCHEME3,
                                         config.SCHEME4, 10,
                                         lambda: print("Purchasing"), remould=False))

        # self.widgets.append(Button(0, 150, shop_width / 3, 50, "Algorithms", 24, config.BLACK,
        #                            config.SCHEME4, config.SCHEME4, 0,
        #                            lambda: print("Checking out algorithms"), shape='rect'))
        # self.widgets.append(Button(shop_width / 3, 150, shop_width / 3, 50, "Upgrades", 24,
        #                            config.BLACK, config.SCHEME4, config.SCHEME4, 0,
        #                            lambda: print("Checking out upgrades"), shape='rect'))
        # self.widgets.append(Button(shop_width / 3 * 2, 150, shop_width / 3, 50, "Businesses", 24,
        #                            config.BLACK, config.SCHEME4, config.SCHEME4, 0,
        #                            lambda: print("Checking out businesses"), shape='rect'))

    def on_enter(self, data, screen):
        print("Shop entered")

    def on_update(self, elapsed):
        super().on_update(elapsed)
