
import numpy as np
import datetime
import pygame
from src import config

from ..widgets import Component, Button, Image, Label, Frame
from ..ml.agents.supervised import ClassificationKNN, NaiveBayes
from ..ml.agents.supervised import LogisticRegression as LogRegAlgo
from ..ml.agents.deeplearning import NeuralNetwork as NeuralNetAlgo
from ..ml.agents.deeplearning import Dense, Activation


class Algorithm(Component):

    def __init__(self, AgentClass, name, environment, w=280, h=150, num_outputs=2):
        super().__init__(0, 0, w, h, name)

        self.agent = AgentClass(environment.num_features)
        self.num_labels = len(environment.get_labels())
        self.num_outputs = num_outputs
        self.render_data = environment.render_data
        self.holder_labels = [x for x in range(self.num_outputs - 1)]  # The last one is an 'other'

        self.train_cooldown = 0
        self.max_train_cooldown = 0

        self.display_shown = True
        self.config_frame = Frame(self.x + self.slot_width * 1.25, self.y + 40,
                                  self.w - self.slot_width * 2.5 - self.slot_height, self.h - 50)
        self.display_frame = Frame(self.x + self.slot_width * 1.25, self.y + 40,
                                   self.w - self.slot_width * 2.5 - self.slot_height, self.h - 50)
        self.add_child(self.config_frame)
        self.add_child(self.display_frame)

        self.skip_elapsed = False

        self.skip_predict = False
        self.predict_cooldown = 0
        self.max_predict_cooldown = 0

        self.place_holders()
        self.setup_inputs_and_outputs()

        self.config_button = Button(0, 0, self.slot_height, self.slot_height,
                                    '', 0, config.BLACK, config.SCHEME3,
                                    config.SCHEME3, 2,
                                    lambda: self.toggle_display(),
                                    shape='rect',
                                    img=Image(0, 0, self.slot_height, self.slot_height,
                                              'config.png'), bsfix=True)

        self.add_child(self.config_button)

        self.setup_percentage_display(environment)

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if self.skip_elapsed:
            self.skip_elapsed = False  # don't count toward timers
        elif self.train_cooldown > 0:
            self.train_cooldown -= elapsed
            self.changed = True
        elif self.predict_cooldown > 0:
            self.predict_cooldown -= elapsed
            self.changed = True
        else:
            in_holder = self.inputs[0]
            if in_holder.has_samples():
                sample = in_holder.take_sample()

                pred_label = self.predict(sample)

                if pred_label in self.holder_labels:
                    self.outputs[self.holder_labels.index(pred_label)].add_sample(sample)
                else:
                    self.outputs[-1].add_sample(sample)

        self.update_percentage_display()

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        if self.display_shown:
            self.config_frame.hide()
            self.display_frame.show()
            self.render_display(screen)  # Must be called every loop
        else:
            self.config_frame.show()
            self.display_frame.hide()

        if self.train_cooldown > 0:
            self.render_train_bar(screen)
        elif self.predict_cooldown > 0:
            self.render_predict_bar(screen)

        for i, holder in enumerate(self.outputs):
            if i >= len(self.holder_labels):
                break

            self.render_data(screen, self.holder_labels[i],
                             np.add(holder.parent.get_pos(True), holder.get_center(True)))

        self.changed = False

    def toggle_display(self):
        self.display_shown = not self.display_shown
        self.changed = True

    def render_train_bar(self, screen):
        perc = self.train_cooldown / self.max_train_cooldown
        width = int(self.w * perc)
        pygame.draw.rect(screen, config.BLUE, (self.x, self.y + 33, width, 5))

    def render_predict_bar(self, screen):
        perc = self.predict_cooldown / self.max_predict_cooldown
        width = int(self.w * perc)
        pygame.draw.rect(screen, config.YELLOW, (self.x, self.y + 33, width, 5))

    def train(self, X, y):
        start_time = datetime.datetime.now()
        self.agent.train(X, y)
        self.skip_elapsed = True
        self.skip_predict = True
        end_time = datetime.datetime.now()

        self.max_train_cooldown = (end_time - start_time).total_seconds()
        self.max_train_cooldown *= 1000 * config.TRAIN_MULTIPLIER
        self.train_cooldown = self.max_train_cooldown

    def _predict(self, sample):
        start_time = datetime.datetime.now()
        pred = self.agent.predict(np.array([sample.x]))
        end_time = datetime.datetime.now()

        if not self.skip_predict:
            self.max_predict_cooldown = (end_time - start_time).total_seconds()
            self.max_predict_cooldown *= 1000 * config.PREDICT_MULTIPLIER
            self.predict_cooldown = self.max_predict_cooldown
        else:
            self.skip_predict = False

        pred_label = int(pred)

        return pred_label

    def place_holders(self):
        title_height = 35
        self.input_pos.append((0, (self.h - title_height) / 2 + title_height))

        for i in range(self.num_outputs):
            top = (self.h - title_height) / self.num_outputs * i
            bottom = (self.h - title_height) / self.num_outputs * (i + 1)
            self.output_pos.append((self.w - self.slot_width, (top + bottom) / 2 + title_height))

            if i >= len(self.holder_labels):
                continue  # Don't want a config button

            index = i
            self.output_button = Button(self.w - self.slot_width - self.slot_height,
                                        (top + bottom) / 2 + title_height - self.slot_height / 2,
                                        self.slot_height,
                                        self.slot_height, '', 0, config.BLACK, config.SCHEME3,
                                        config.SCHEME3, 2,
                                        lambda: self.change_label(index),
                                        shape='rect',
                                        img=Image(0, 0, self.slot_height, self.slot_height,
                                                  'config.png'), bsfix=True)
            self.add_child(self.output_button)

    def change_label(self, i):
        self.holder_labels[i] += 1
        if self.holder_labels[i] >= self.num_labels:
            self.holder_labels[i] = 0
        self.changed = True

    def render_display(self, screen):
        # Allows for different displays to be added in future
        # Just turns out it's quite hard for 1 of 2 reasons
        # Most data is not 2D
        # Neural nets are basically black boxes
        self.render_percentage_display(screen)

    def setup_percentage_display(self, environment):
        self.output_rects = []
        self.output_predictions = [0 for x in range(environment.num_labels)]
        self.output_totals = [0 for x in range(environment.num_labels)]

        width = (self.w - self.slot_width * 2.5 - self.slot_height) / environment.num_labels
        for i in range(environment.num_labels):
            self.output_rects.append(Label(width * i, 60, width, 80,
                                           None, '--%', 26, config.WHITE))

        for rect in self.output_rects:
            self.display_frame.add_child(rect)

    def render_percentage_display(self, screen):
        for i, rect in enumerate(self.output_rects):
            self.render_data(screen, i,
                             np.add(np.add(rect.get_center(True), self.get_pos(True)),
                                    (int(self.display_frame.x), 0)))

    def update_percentage_display(self):
        for i, rect in enumerate(self.output_rects):
            rect.change_text(self.get_perc_string(self.output_predictions[i],
                             self.output_totals[i]))

    def predict(self, sample):
        pred_label = self._predict(sample)

        self.output_totals[int(sample.y)] += 1
        if pred_label == int(sample.y):
            self.output_predictions[pred_label] += 1

        return pred_label

    def get_perc_string(self, numerator, denominator):
        if denominator == 0:
            return '--%'
        dp = int(numerator / denominator * 100)
        return str(dp) + '%'


class KNN(Algorithm):

    def __init__(self, environment):
        super().__init__(ClassificationKNN, 'KNN', environment, w=280)

        self.config_frame.add_child(Label(20, 0, 100, 30, None, "Nearest", 22, config.BLACK))
        self.k_display = Label(20, 40, 100, 60, None, str(self.agent.k), 72, config.BLACK)
        self.config_frame.add_child(self.k_display)

        self.config_frame.add_child(Button(110, 40, 30, 30, "/\\", 30, config.GREEN,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_k(1), shape='rect', bsfix=True))
        self.config_frame.add_child(Button(110, 70, 30, 30, "\\/", 30, config.BLUE,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_k(-1), shape='rect', bsfix=True))

    def change_k(self, val):
        self.agent.k += val
        self.agent.k = max(1, self.agent.k)
        self.k_display.change_text(str(self.agent.k))

        # width = self.w - self.slot_width * 2.5 - self.slot_height
        # canvas = pygame.Surface((width, self.h - 50))
        # canvas.fill(config.WHITE)
        # pygame.draw.rect(canvas, config.BLACK, (10, 10, 30, 30))
        #
        # screen.blit(canvas, (self.x + self.slot_width * 1.25, self.y + 40))


class NBayes(Algorithm):

    def __init__(self, environment):
        super().__init__(NaiveBayes, 'N Bayes', environment, w=280)


class LogisticRegression(Algorithm):

    def __init__(self, environment):
        super().__init__(LogRegAlgo, 'Log Reg', environment, w=280)

        self.config_frame.add_child(Label(20, 0, 100, 30, None, "Train Amt", 22, config.BLACK))
        self.iter_display = Label(20, 40, 100, 60, None,
                                  str(self.agent.num_iters // 200), 72, config.BLACK)
        self.config_frame.add_child(self.iter_display)

        self.config_frame.add_child(Button(110, 40, 30, 30, "/\\", 30, config.GREEN,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_iters(1), shape='rect', bsfix=True))
        self.config_frame.add_child(Button(110, 70, 30, 30, "\\/", 30, config.BLUE,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_iters(-1), shape='rect', bsfix=True))

    def change_iters(self, val):
        self.agent.num_iters += val * 200
        self.agent.num_iters = max(self.agent.num_iters, 200)
        self.iter_display.change_text(str(self.agent.num_iters // 200))


class NeuralNetwork(Algorithm):

    def __init__(self, environment):
        super().__init__(NeuralNetAlgo, 'Neural Net', environment, w=280)

        self.layers = 2
        self.num_features = environment.num_features
        self.num_labels = environment.num_labels

        self.agent.add_layer(Dense(10, input_shape=environment.num_features))
        self.agent.add_layer(Activation('sigmoid'))
        self.agent.add_layer(Dense(environment.num_labels))
        self.agent.add_layer(Activation('softmax'))

        self.setup_train_config()

    def setup_train_config(self):
        self.config_frame.add_child(Label(0, 0, 65, 50, None, "Train", 18, config.BLACK))
        self.iter_display = Label(75, 0, 30, 50, None,
                                  str(self.agent.num_iters // 200), 26, config.BLACK)
        self.config_frame.add_child(self.iter_display)

        self.config_frame.add_child(Button(110, 0, 25, 25, "/\\", 18, config.GREEN,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_iters(1), shape='rect', bsfix=True))
        self.config_frame.add_child(Button(110, 25, 25, 25, "\\/", 18, config.BLUE,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_iters(-1), shape='rect', bsfix=True))

        layer_y = 50
        self.config_frame.add_child(Label(0, layer_y, 65, 50, None, "Layers", 18, config.BLACK))
        self.layer_display = Label(75, layer_y, 30, 50, None,
                                   str(len(self.agent.layers) // 2), 26, config.BLACK)
        self.config_frame.add_child(self.layer_display)

        self.config_frame.add_child(Button(110, layer_y, 25, 25, "/\\", 18, config.GREEN,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_layer(1), shape='rect', bsfix=True))
        self.config_frame.add_child(Button(110, layer_y + 25, 25, 25, "\\/", 18, config.BLUE,
                                           config.SCHEME4, config.SCHEME4, 0,
                                           lambda: self.change_layer(-1), shape='rect', bsfix=True))

    def change_iters(self, val):
        self.agent.num_iters += 200 * val
        self.agent.num_iters = max(self.agent.num_iters, 200)
        self.iter_display.change_text(str(self.agent.num_iters // 200))

    def change_layer(self, val):
        self.layers = self.layers + val
        self.layers = max(1, self.layers)

        self.agent.clear_layers()

        for i in range(self.layers - 1):
            self.agent.add_layer(Dense(self.num_features, input_shape=self.num_features))
            self.agent.add_layer(Activation('relu'))
        self.agent.add_layer(Dense(self.num_labels, input_shape=self.num_features))
        self.agent.add_layer(Activation('softmax'))

        self.layer_display.change_text(str(len(self.agent.layers) // 2))
