
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
        self.add_child(self.config_frame)

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

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

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

    def predict(self, sample):
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

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        if self.display_shown:
            self.config_frame.hide()
            self.render_display(screen)
        else:
            self.config_frame.show()

    def change_k(self, val):
        self.agent.k += val
        self.agent.k = max(1, self.agent.k)
        self.k_display.change_text(str(self.agent.k))

    def render_display(self, screen):
        width = self.w - self.slot_width * 2.5 - self.slot_height
        canvas = pygame.Surface((width, self.h - 50))
        canvas.fill(config.WHITE)
        pygame.draw.rect(canvas, config.BLACK, (10, 10, 30, 30))

        screen.blit(canvas, (self.x + self.slot_width * 1.25, self.y + 40))


class NBayes(Algorithm):

    def __init__(self, environment):
        super().__init__(NaiveBayes, 'N Bayes', environment, w=280)


class LogisticRegression(Algorithm):

    def __init__(self, environment):
        super().__init__(LogRegAlgo, 'Log Reg', environment, w=280)


class NeuralNetwork(Algorithm):

    def __init__(self, environment):
        super().__init__(NeuralNetAlgo, 'Neural Net', environment, w=280)

        self.agent.add_layer(Dense(10, input_shape=environment.num_features))
        self.agent.add_layer(Activation('sigmoid'))
        self.agent.add_layer(Dense(environment.num_labels))
        self.agent.add_layer(Activation('softmax'))

        self.output_rects = []
        self.output_predictions = [0 for x in range(environment.num_labels)]
        self.output_totals = [0 for x in range(environment.num_labels)]

        width = (self.w - self.slot_width * 2.5 - self.slot_height) / environment.num_labels
        for i in range(environment.num_labels):
            self.output_rects.append(Label(self.slot_width * 1.25 + width * i, 60, width, 80,
                                           None, '--%', 26, config.WHITE))

        for rect in self.output_rects:
            self.add_child(rect)

    def on_update(self, elapsed):
        super().on_update(elapsed)

        for i, rect in enumerate(self.output_rects):
            rect.change_text(self.get_perc_string(self.output_predictions[i],
                             self.output_totals[i]))

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        for i, rect in enumerate(self.output_rects):
            self.render_data(screen, i,
                             np.subtract(np.add(rect.get_center(True), self.get_pos(True)),
                                         (0, 40)))

    def predict(self, sample):
        pred_label = super().predict(sample)  # Ahem Python

        self.output_totals[int(sample.y)] += 1
        if pred_label == int(sample.y):
            self.output_predictions[pred_label] += 1

        return pred_label

    def get_perc_string(self, numerator, denominator):
        if denominator == 0:
            return '--%'
        dp = int(numerator / denominator * 100)
        return str(dp) + '%'
