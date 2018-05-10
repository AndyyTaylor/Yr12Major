" Andy "
import abc


class UIElement(metaclass=abc.ABCMeta):
    " This class is inherited by all ui elements "

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abc.abstractmethod
    def on_update(self, elapsed):
        pass

    @abc.abstractmethod
    def on_render(self, screen):
        pass

    def on_mouse_motion(self, pos):
        return

    def get_pos(self):
        return (self.x, self.y)

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def get_center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_adj_center(self, x_off, y_off):
        return (self.x + self.w / 2 - x_off, self.y + self.h / 2 - y_off)
