
from .screen import Screen

import pygame
import copy

from src import config
from ..elements import Textbox
from ..components import *
from ..machines import *
from ..machines.machine import Machine
from .screen import Screen


class LevelState(Screen):  # Download CLION's Python IDE, they also do a C/C++ one
    " A "

    def __init__(self):
        super().__init__("Level", "MasterState")

        self.connections = []
        self.elements = []

        self.input = None
        self.output = None
        self.playing = False
        self.past_level = None

        play_button = Button.create_rounded_image_button(
                        1200, 110, 70, 70, config.BLACK, config.SCHEME2, 3,
                        1220, 130, 30, 30, "data/assets/play.png", self.play
        )
        pause_button = Button.create_rounded_image_button(
                        1280, 110, 70, 70, config.BLACK, config.SCHEME2, 3,
                        1300, 130, 30, 30, "data/assets/pause.png", self.pause
        )
        stop_button = Button.create_rounded_image_button(
                        1360, 110, 70, 70, config.BLACK, config.SCHEME2, 3,
                        1380, 130, 30, 30, "data/assets/stop.png", self.stop
        )

        self.components = [
            play_button,
            pause_button,
            stop_button
        ]

    def on_enter(self, data, screen):
        assert isinstance(data, int)
        super().on_enter(data, screen)

        if self.past_level is None or self.past_level != data:
            if self.past_level is not None:
                for i in range(2):
                    self.components.pop()  # The last 'element' should always be the level title
                                           # and the second last should be the workshop

            self.past_level = data
            self.playing = False

            self.create_title(data)

            self.connections = []
            self.components.append(self.create_workshop(data))

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if self.playing:
            for conn in self.connections:
                conn.on_update(elapsed)

            if self.game_finished():
                config.MAX_LEVEL += 1
                self.parent.change_state("LevelSelector")

    def game_finished(self):
        # Game is finished if everything is empty
        # for c in self.connections + self.machines:
        #     if c.has_data():
        #         return False
        # return True
        return False

    def on_render(self, screen):
        super().on_render(screen)

    def play(self):
        self.playing = True
        print("play")
        # for comp in self.machines:
        #     comp.train(*self.input.get_train_data())

    def pause(self):
        self.playing = False

    def stop(self):
        print("Stop not implemented")

    def on_mouse_down(self, event, pos):
        for component in self.components:
            component.on_mouse_down(pos)

    def on_mouse_motion(self, event, pos):
        for component in self.components:
            # if isinstance(component, Machine) and component.clicked and component.cloneable:
            #     component.clicked = False
            #
            #     self.machines.append(component.clone(pos, self.input.get_labels(), self.input.render_data))
            # else:
            component.on_mouse_motion(pos)

    def on_mouse_up(self, event, pos):
        return
        # input_holder = None
        # output_holder = None
        # for machine in self.machines:
        #     input, output = machine.on_mouse_up(pos)
        #
        #     if input is not None:  # does this implicitly check if not none?
        #         output_holder = input
        #     if output is not None:
        #         input_holder = output
        #
        # if input_holder is not None and output_holder is not None:
        #     self.connections.append(Connection(input_holder, output_holder, self.input.render_data))

    def create_title(self, level_num):
        self.components.append(Header.create_rectangle_header(
                                0, 0, config.SCREEN_WIDTH, 100, config.SCHEME2,
                                "Level " + str(level_num), config.BLACK, 72)
                              )

    def create_workshop(self, level_num):
        input, output = self.load_level(level_num)

        trash = Trash()
        naivebayes = NaiveBayes(input.get_labels(), input.render_data)
        knn = KNN(input.get_labels(), input.render_data)

        algorithms = [
            trash,
            naivebayes,
            knn
        ]
        return Workshop(0, 120, 300, 740, input, output, algorithms)

    def load_level(self, level_num):
        if level_num == 1:
            input = ColorInput(2)
            output = Output(0, input.render_data)
        elif level_num == 2:
            input = ColorInput(3)
            output = Output(1, input.render_data)
        elif level_num == 3:
            input = ShapeInput(4)
            output = Output(4, input.render_data)
        else:
            raise NotImplementedError("Don't got that level")

        return input, output
