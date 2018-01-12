" Andy "
import abc

class State(metaclass=abc.ABCMeta):
    " The abstract class that all states inherit "

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def on_init(self):
        " Called when the application is run "
        return

    @abc.abstractmethod
    def on_shutdown(self):
        " Called when the application is closed "
        return

    @abc.abstractmethod
    def on_enter(self):
        " Called when the state is entered "
        return

    @abc.abstractmethod
    def on_exit(self):
        " Called when the state is exited "
        return

    @abc.abstractmethod
    def on_update(self, elapsed):
        " Called as fast as possible "
        return

    @abc.abstractmethod
    def on_render(self):
        " Called on render "
        return
