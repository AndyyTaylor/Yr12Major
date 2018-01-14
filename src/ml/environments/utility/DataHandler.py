from .Point import Point

class DataHandler:
    def __init__(self, gen_function, points):
        self.data = []

        self.gen_function = gen_function

        self.gen_data(points)

    def gen_data(self, points):
        for i in range(points): # pylint: disable=W0612
            x, y = self.gen_function()
            self.data.append(Point(x, y))

    def add_data_point(self, x, y):
        self.data.append(Point(x, y))

    def clear_data(self):
        self.data = []

    def get_points(self):
        return self.data
