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

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)
