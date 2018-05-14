" Andy "


class UIElement():
    " This class is inherited by all ui elements "

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.changed = True

    def on_update(self, elapsed):
        pass

    def on_render(self, screen):
        self.changed = False

    def on_mouse_motion(self, pos):
        return

    def reset_animation(self):
        return

    def has_changed(self):
        return self.changed

    def get_pos(self):
        return (self.x, self.y)

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def get_center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_adj_center(self, x_off, y_off):
        return (self.x + self.w / 2 - x_off, self.y + self.h / 2 - y_off)
