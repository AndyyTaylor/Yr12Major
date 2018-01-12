" Andy "
import abc

class State(abc.ABCMETA):
    " The abstract class that all states inherit "

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
