" Andy "

from ..framework.StateRegistry import StateRegistry

class State():
    " The abstract class that all states inherit "

    def __init__(self, name, parent):
        self.name = name
        self.parent = StateRegistry.instance().register(self, parent)

    def on_init(self):
        " Called when the application is run "
        return

    def on_shutdown(self):
        " Called when the application is closed "
        return

    def on_enter(self):
        " Called when the state is entered "
        return

    def on_exit(self):
        " Called when the state is exited "
        return

    def on_update(self, elapsed):
        " Called as fast as possible "
        return

    def on_render(self, screen):
        " Called on render "
        return

    def on_mouse_down(self, pos):
        " Passed the mouse position "
        return
