
from ..widgets import Component


class Sample:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.progress = 0


class Input(Component):

    def __init__(self, x, y, environment):
        super().__init__(x, y, 280, 150, 'Input')

        self.environment = environment

        self.output_pos.append((self.w - self.slot_width, self.h / 2))
        self.setup_inputs_and_outputs()

        self.load_samples()

    def on_render(self, screen, back_fill=None):
        super().on_render(screen, back_fill)

        y_m = 35  # top_margin
        l_x_m = 10
        r_x_m = 50
        labels = self.environment.get_labels()
        num_labels = len(labels)
        for i, label in enumerate(labels):  # Figure this shit out
            label_w = (self.w - l_x_m - r_x_m) / num_labels
            label_w = min(self.h - y_m, label_w)
            self.environment.render_data(screen, label,
                                         (int(self.x + l_x_m + label_w * (i + 0.5)),
                                          self.y + y_m + int((self.h - y_m) / 2)),
                                         int(label_w / 2))  # Size is in radius

    def load_samples(self):
        for i in range(self.environment.testX.shape[0]):
            sample = Sample(self.environment.testX[i], self.environment.testy[i])
            self.outputs[0].add_sample(sample)

    def get_train_data(self):
        return (self.environment.trainX, self.environment.trainy)

    def get_labels(self):
        return self.environment.get_labels()

    def clear_holders(self):
        super().clear_holders()

        self.load_samples()
