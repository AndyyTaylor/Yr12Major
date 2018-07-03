
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

        for i in range(self.environment.testX.shape[0]):
            sample = Sample(self.environment.testX[i], self.environment.testy[i])
            self.outputs[0].add_sample(sample)

    def get_train_data(self):
        return (self.environment.trainX, self.environment.trainy)

    def get_labels(self):
        return self.environment.get_labels()
