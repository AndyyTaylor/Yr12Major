
import numpy as np
from src import config

from ..widgets import Component, Button, Image
from ..ml.agents.supervised import ClassificationKNN, NaiveBayes
from ..ml.agents.supervised import LogisticRegression as LogRegAlgo


class Algorithm(Component):

    def __init__(self, AgentClass, name, environment, w=280, h=150, num_outputs=2):
        super().__init__(0, 0, w, h, name)

        self.agent = AgentClass(environment.num_features)
        self.num_labels = len(environment.get_labels())
        self.num_outputs = num_outputs
        self.render_data = environment.render_data
        self.holder_labels = [x for x in range(self.num_outputs - 1)]  # The last one is an 'other'

        self.place_holders()
        self.setup_inputs_and_outputs()

    def on_mouse_down(self, pos):
        super().on_mouse_down(pos)

        print("Mouse down")

    def on_update(self, elapsed):
        super().on_update(elapsed)
        # print(self.output_button.get_pos())
        in_holder = self.inputs[0]
        if in_holder.has_samples():
            sample = in_holder.take_sample()

            pred = self.agent.predict(np.array([sample.x]))
            pred_label = int(pred)

            if pred_label in self.holder_labels:
                self.outputs[self.holder_labels.index(pred_label)].add_sample(sample)
            else:
                self.outputs[-1].add_sample(sample)

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        for i, holder in enumerate(self.outputs):
            if i >= len(self.holder_labels):
                break

            self.render_data(screen, self.holder_labels[i],
                             np.add(holder.parent.get_pos(True), holder.get_center(True)))

    def train(self, X, y):
        self.agent.train(X, y)

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
        self.outputs[i].changed = True


class KNN(Algorithm):

    def __init__(self, environment):
        super().__init__(ClassificationKNN, 'KNN', environment, w=150)


class NBayes(Algorithm):

    def __init__(self, environment):
        super().__init__(NaiveBayes, 'N Bayes', environment, w=150)


class LogisticRegression(Algorithm):

    def __init__(self, environment):
        super().__init__(LogRegAlgo, 'Log Reg', environment, w=200)
