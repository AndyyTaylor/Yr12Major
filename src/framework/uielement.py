
class UIElement():

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_pos(self):
        return (self.x, self.y)

    def get_size(self):
        return (self.w, self.h)

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def get_prev_rect(self):
        return self.prev_rect

    def get_center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_adj_center(self, x_off, y_off):
        return (self.x + self.w / 2 - x_off, self.y + self.h / 2 - y_off)
