
import pygame
from src import config
from .screen import Screen
from ..widgets import Button, Frame, Label


class Shop(Screen):

    def __init__(self):
        super().__init__("Shop", "MasterState")

        # I'm convinced I'm forgetting some stuff that will go on this screen

        shop_width = config.SCREEN_WIDTH

        self.shop_frame = Frame(0, 200, shop_width, config.SCREEN_HEIGHT - 200, True,
                                config.SCHEME5, grid_type='grid', item_x_margin=80)
        self.widgets.append(self.shop_frame)

        # This should be loaded from the config later, or somewhere
        self.purchases = {
            'algorithms': [
                {
                    'name': 'KNN',
                    'cost': 1000,
                    'blurb': 'Lazy classifier that attempts to find similarities \
                              between training and test data'
                }, {
                    'name': 'Naive Bayes',
                    'cost': 10000,
                    'blurb': 'Fast statistical classifier'
                }
            ], 'upgrades': [

            ], 'businesses': [

            ]
        }

        self.create_purchase_buttons()
        self.create_title_buttons()

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

    def create_purchase_buttons(self):
        for type, items in self.purchases.items():
            # Type will determine which frame is used
            for item in items * 5:
                self.shop_frame.add_child(self.create_shop_item(item))

    def create_shop_item(self, item):
        size = 300

        item_frame = Frame(0, 0, 300, 300)
        item_frame.add_child(Button(0, 0, size, size, '', 24, config.BLACK, config.SCHEME3,
                                    config.SCHEME4, 10, lambda: print("Purchasing something"),
                                    remould=False))
        item_frame.add_child(Label(0, 10, 300, 50, None, item['name'], 36, config.SCHEME1))
        item_frame.add_child(Label(0, 50, 300, 40, None,
                                   '$ ' + str(item['cost']), 36, config.GREEN))

        return item_frame

    def create_title_buttons(self):
        self.widgets.append(Button(0, 150, config.SCREEN_WIDTH / 3, 50, "Algorithms", 24,
                                   config.BLACK, config.SCHEME4, config.SCHEME4, 0,
                                   lambda: print("Checking out algorithms"), shape='rect'))
        self.widgets.append(Button(config.SCREEN_WIDTH / 3, 150, config.SCREEN_WIDTH / 3, 50,
                                   "Upgrades", 24, config.BLACK, config.SCHEME4, config.SCHEME4, 0,
                                   lambda: print("Checking out upgrades"), shape='rect'))
        self.widgets.append(Button(config.SCREEN_WIDTH / 3 * 2, 150, config.SCREEN_WIDTH / 3, 50,
                                   "Businesses", 24, config.BLACK, config.SCHEME4, config.SCHEME4,
                                   0, lambda: print("Checking out businesses"), shape='rect'))

    def on_update(self, elapsed):
        super().on_update(elapsed)
