
import pygame
from src import config
from .screen import Screen
from ..widgets import Button, Frame, Label, Message


class Shop(Screen):

    def __init__(self):
        super().__init__("Shop", "MasterState")

        # I'm convinced I'm forgetting some stuff that will go on this screen

        shop_width = config.SCREEN_WIDTH

        self.algorithm_frame = Frame(0, 200, shop_width, config.SCREEN_HEIGHT - 200, True,
                                     config.SCHEME5, grid_type='grid', item_x_margin=80)
        self.upgrade_frame = Frame(0, 200, shop_width, config.SCREEN_HEIGHT - 200, True,
                                   config.SCHEME5, grid_type='grid', item_x_margin=80)
        self.business_frame = Frame(0, 200, shop_width, config.SCREEN_HEIGHT - 200, True,
                                    config.SCHEME5, grid_type='grid', item_x_margin=80)

        self.upgrade_frame.hide()
        self.business_frame.hide()

        self.widgets.append(self.algorithm_frame)
        self.widgets.append(self.upgrade_frame)
        self.widgets.append(self.business_frame)

        self.title_frame.add_child(Label(config.SCREEN_WIDTH - 300, 0, 300, 60, None, "You Have",
                                         48, config.BLACK))
        self.balance_label = Label(config.SCREEN_WIDTH - 300, 70, 300, 60, config.SCHEME2, "$" +
                                   str(config.MONEY), 48, config.BLACK)
        self.title_frame.add_child(self.balance_label)

        # This should be loaded from the config later, or somewhere
        self.purchases = {
            'algorithm': [
                {
                    'name': 'Logistic Regression',
                    'cost': 0,
                    'blurb': 'Creates approximate functions to create estimates'
                }, {
                    'name': 'KNN',
                    'cost': 1000,
                    'blurb': 'Lazy classifier that finds similar examples that it was shown during training'  # noqa
                }, {
                    'name': 'Naive Bayes',
                    'cost': 2000,
                    'blurb': 'Fast statistical classifier that models data using gaussian distributions'  # noqa
                }, {
                    'name': 'Neural Network',
                    'cost': 999999,
                    'blurb': 'Extremely versatile classifier built using layers'
                }, {
                    'name': 'Policy Gradient',
                    'cost': 99999,
                    'blurb': 'Basic RL Algorithm'
                }, {
                    'name': 'Other RL',
                    'cost': 99999,
                    'blurb': 'Another basic RL algorithm'
                }, {
                    'name': 'Q Learning',
                    'cost': 9999,
                    'blurb': 'Q Learning is a more advanced RL Algorithm'
                }
            ], 'upgrade': [
                {
                    'name': 'Degree 2',
                    'cost': 9999,
                    'blurb': 'Allows logistic regression to create 2nd degree functions'
                }, {
                    'name': 'Degree 3',
                    'cost': 9999,
                    'blurb': 'Allows logistic regression to create 3rd degree functions'
                }, {
                    'name': 'Degree 4',
                    'cost': 9999,
                    'blurb': 'Allows logistic regression to create 4th degree functions'
                }
            ], 'businesse': [

            ]
        }

        self.create_purchase_buttons()
        self.create_title_buttons()

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

    def create_purchase_buttons(self):
        for type, items in self.purchases.items():
            for item in items:
                if type == 'algorithm':
                    self.algorithm_frame.add_child(self.create_shop_item(item))
                elif type == 'upgrade':
                    self.upgrade_frame.add_child(self.create_shop_item(item))
                else:
                    self.business_frame.add_child(self.create_shop_item(item))

    def create_shop_item(self, item):
        size = 300

        item_frame = Frame(0, 0, 300, 300)
        item_frame.add_child(Button(0, 0, size, size, '', 24, config.BLACK, config.SCHEME3,
                                    config.SCHEME4, 10, lambda: self.purchase(item),
                                    remould=False))
        item_frame.add_child(Label(0, 10, 300, 50, None, item['name'], 24, config.SCHEME1))
        item_frame.add_child(Label(0, 50, 300, 40, None,
                                   '$ ' + str(item['cost']), 36, config.GREEN))
        item_frame.add_child(Message(10, 100, 280, 170, None, item['blurb'], 18, config.BLACK,
                                     align='ll'))

        return item_frame

    def create_title_buttons(self):
        self.widgets.append(Button(0, 150, config.SCREEN_WIDTH / 3, 50, "Algorithms", 24,
                                   config.BLACK, config.SCHEME4, config.SCHEME4, 0,
                                   lambda: self.show_algorithms(), shape='rect'))
        self.widgets.append(Button(config.SCREEN_WIDTH / 3, 150, config.SCREEN_WIDTH / 3, 50,
                                   "Upgrades", 24, config.BLACK, config.SCHEME4, config.SCHEME4, 0,
                                   lambda: self.show_upgrades(), shape='rect'))
        self.widgets.append(Button(config.SCREEN_WIDTH / 3 * 2, 150, config.SCREEN_WIDTH / 3, 50,
                                   "Businesses", 24, config.BLACK, config.SCHEME4, config.SCHEME4,
                                   0, lambda: self.show_businesses(), shape='rect'))

    def show_algorithms(self):
        self.algorithm_frame.show()
        self.upgrade_frame.hide()
        self.business_frame.hide()

    def show_upgrades(self):
        self.algorithm_frame.hide()
        self.upgrade_frame.show()
        self.business_frame.hide()

    def show_businesses(self):
        self.algorithm_frame.hide()
        self.upgrade_frame.hide()
        self.business_frame.show()

    def on_update(self, elapsed):
        super().on_update(elapsed)

        self.balance_label.change_text("$" + str(config.MONEY))

    def purchase(self, item):
        if item['name'] not in config.PURCHASES:
            if item['cost'] < config.MONEY:
                config.MONEY -= item['cost']
                config.PURCHASES.append(item['name'])
