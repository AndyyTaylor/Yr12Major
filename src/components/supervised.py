
import numpy as np

from ..widgets import Component
from ..ml.agents.supervised import ClassificationKNN


class Algorithm(Component):

    def __init__(self, AgentClass, name, environment, w=280, h=150, num_outputs=3):
        super().__init__(0, 0, w, h, name)

        self.agent = AgentClass(environment.num_features)
        self.num_outputs = num_outputs
        self.render_data = environment.render_data
        self.holder_labels = [x for x in range(self.num_outputs - 1)]  # The last one is an 'other'

        self.place_holders()
        self.setup_inputs_and_outputs()

    def on_update(self, elapsed):
        super().on_update(elapsed)

        in_holder = self.inputs[0]
        if in_holder.has_samples():
            sample = in_holder.take_sample()

            pred = self.agent.predict(sample)

            print('Prediction:', pred)

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


class KNN(Algorithm):

    def __init__(self, environment):
        super().__init__(ClassificationKNN, 'KNN', environment, w=150)
