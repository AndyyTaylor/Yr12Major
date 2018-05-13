
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
        self.past_level = None

        self.elements.append(Textbox(0, 130, 300, 50, "Components", config.BLACK, 36))

        self.elements.append(RoundedButton(1360, 110, 70, 70, 3, config.BLACK, config.SCHEME2, lambda: print("Stop")))
        self.elements.append(Image(1380, 130, 30, 30, "data/assets/stop.png"))
        self.elements.append(RoundedButton(1280, 110, 70, 70, 3, config.BLACK, config.SCHEME2, self.pause))
        self.elements.append(Image(1300, 130, 30, 30, "data/assets/pause.png"))
        self.elements.append(RoundedButton(1200, 110, 70, 70, 3, config.BLACK, config.SCHEME2, self.play))
        self.elements.append(Image(1220, 130, 30, 30, "data/assets/play.png"))

    def on_enter(self, data):
        assert isinstance(data, int)

        if self.past_level is None or self.past_level != data:
            if self.past_level is not None:
                self.elements.pop()  # The last 'element' should always be the level title

            self.past_level = data
            self.playing = False

            self.elements.append(Textbox(0, 0, config.SCREEN_WIDTH, 100,
                                         "LEVEL " + str(data), config.BLACK, 72))

            self.components = []
            self.connections = []
            self.load_level(data)
            self.load_components()

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

            if self.game_finished():
                config.MAX_LEVEL += 1
                self.parent.change_state("LevelSelector")

    def game_finished(self):
        # Game is finished if everything is empty
        for c in self.connections + self.components:
            if c.has_data():
                return False

        return True

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
            if isinstance(component, Component) and component.clicked and component.cloneable:
                component.clicked = False

                self.components.append(component.clone(pos, self.input.get_labels(), self.input.render_data))
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

    def load_components(self):
        self.components.append(self.input)
        self.components.append(self.output)
        self.components.append(Trash())
        self.components.append(NaiveBayes(self.input.get_labels(), self.input.render_data))
        self.components.append(KNN(self.input.get_labels(), self.input.render_data))

    def load_level(self, level_num):
        if level_num == 1:
            self.input = ColorInput(2)
            self.output = Output(0, self.input.render_data)
        elif level_num == 2:
            self.input = ColorInput(3)
            self.output = Output(1, self.input.render_data)
        elif level_num == 3:
            self.input = ShapeInput(4)
            self.output = Output(4, self.input.render_data)
        else:
            raise NotImplementedError("Don't got that level")
