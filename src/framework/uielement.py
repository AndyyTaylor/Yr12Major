
class UIElement():

    def __init__(self, x, y, w, h):
        self.w = w
        self.h = h

        self.set_pos(x, y)

        self.prev_x = x
        self.prev_y = y

    def get_pos(self):
        return (self.x, self.y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def update_prev_pos(self):
        self.prev_x = self.x
        self.prev_y = self.y

    def sub_pos(self, dx, dy):
        self.x -= dx
        self.y -= dy

    def add_pos(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_size(self):
        return (self.w, self.h)

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def get_prev_rect(self):
        return (self.prev_x, self.prev_y, self.w, self.h)

    def get_center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_adj_center(self, x_off, y_off):
        return (self.x + self.w / 2 - x_off, self.y + self.h / 2 - y_off)
