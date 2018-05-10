
from .AbstractState import State

import pygame
import copy

from .. import config
from ..components import *
from ..ml.environments.game import *
from ..ui import RoundedButton


class LevelState(State):
    " A "

    def __init__(self):
        super().__init__("Level", "MasterState")

        self.components = []
        self.connections = []
        self.elements = []

        self.input = None
        self.output = None
        self.playing = False

        # self.elements.append(Textbox(0, 0, config.SCREEN_WIDTH, 100, "LEVEL 1", config.BLACK, 72))  # HARDCODED
        self.elements.append(Textbox(0, 130, 300, 50, "Components", config.BLACK, 36))

        self.elements.append(RoundedButton(1360, 110, 70, 70, 3, config.BLACK, config.SCHEME2, lambda: print("Stop")))
        self.elements.append(RoundedButton(1280, 110, 70, 70, 3, config.BLACK, config.SCHEME2, self.pause))
        self.elements.append(RoundedButton(1200, 110, 70, 70, 3, config.BLACK, config.SCHEME2, self.play))

    def on_enter(self, data):
        print("Level " + str(data) + " entered")
        self.elements.append(Textbox(0, 0, config.SCREEN_WIDTH, 100, "LEVEL " + str(data), config.BLACK, 72))

        self.load_level(data)
        self.components.append(self.input)
        self.components.append(self.output)
        self.components.append(Trash())
        self.components.append(NaiveBayes(self.input.get_labels(), self.input.render_data))
        self.components.append(KNN(self.input.get_labels(), self.input.render_data))

        cum_y = 20
        for i in range(len(self.components)):
            self.components[i].set_pos(50, 180 + cum_y)
            cum_y += 10 + self.components[i].h

    def on_update(self, elapsed):
        for elem in self.elements:
            elem.on_update(elapsed)

        if self.playing:
            for conn in self.connections:
                conn.on_update(elapsed)

            for comp in self.components:
                comp.on_update(elapsed)

    def on_render(self, screen):
        screen.fill(config.SCHEME5)

        pygame.draw.rect(screen, config.SCHEME2, (0, 0, config.SCREEN_WIDTH, 100))
        pygame.draw.rect(screen, config.SCHEME2, (0, 0, 300, config.SCREEN_HEIGHT))

        pygame.draw.rect(screen, config.SCHEME5, (0, 100, 500, 20))

        for elem in self.connections + self.elements + self.components:
            elem.on_render(screen)

    def play(self):
        self.playing = True

        for comp in self.components:
            comp.train(*self.input.get_train_data())

    def pause(self):
        self.playing = False

    def on_mouse_down(self, event, pos):
        for component in self.components + self.elements:
            component.on_mouse_down(pos)

    def on_mouse_motion(self, event, pos):
        for component in self.components + self.elements:
            if isinstance(component, Component) and component.clicked and component.clone:
                component.clicked = False
                if isinstance(component, Algorithm):
                    new_comp = component.__class__(self.input.get_labels(), self.input.render_data)
                else:
                    new_comp = component.__class__()
                new_comp.clicked = True
                new_comp.clone = False
                new_comp.set_pos(*component.get_pos())
                new_comp.mouse_offset_x = pos[0] - new_comp.x
                new_comp.mouse_offset_y = pos[1] - new_comp.y

                self.components.append(new_comp)
                print("Cloned")
            else:
                component.on_mouse_motion(pos)

    def on_mouse_up(self, event, pos):
        input_holder = None
        output_holder = None
        for component in self.components:
            input, output = component.on_mouse_up(pos)

            if input is not None:  # does this implicitly check if not none?
                output_holder = input
            if output is not None:
                input_holder = output

        if input_holder is not None and output_holder is not None:
            self.connections.append(Connection(input_holder, output_holder, self.input.render_data))

    def load_level(self, level_num):
        if level_num == 1:
            self.input = ColorInput(2)
            self.output = ColorOutput(2, self.input.render_data)
        elif level_num == 2:
            self.input = ColorInput(3)
            self.output = ColorOutput(3, self.input.render_data)
        else:
            raise NotImplementedError("Don't got that level")
