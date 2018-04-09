" doc "

from ..framework.StateRegistry import StateRegistry
from ..states.AbstractState import State


class StateGroup(State):
    " doc "

    def __init__(self, name, parent=False):
        self.name = name
        self.state_stack = []
        self.children = {}  # should this be array and get instance from registry?
        self.parent = False
        self.default = None

        StateRegistry.instance().register_group(self)
        if parent:
            self.parent = StateRegistry.instance().get_group(parent)
            self.parent.add_child(self)
        elif name != "MasterState":
            self.parent = StateRegistry.instance().get_group("MasterState")
            self.parent.add_child(self)

    def add_child(self, child):
        if not self.children:
            self.default = child
        self.children[child.name] = child

    def change_state(self, name, data=()):
        StateRegistry.instance().push_stack(data)

        if self.state_stack:
            self.state_stack.pop().on_exit()

        self.state_stack = []

        if name in self.children:
            self.children[name].on_enter(StateRegistry.instance().pop_stack())
            self.state_stack.append(self.children[name])
        else:
            self.parent.change_state(name)

    def push_state(self, new_state):
        state = StateRegistry.instance().get_state(new_state)
        state.on_enter()

        self.state_stack.append(state)

    def pop_state(self):
        if self.state_stack:
            self.state_stack.pop().on_exit()

    def reset_stack(self):
        self.state_stack.append(self.default)

    def get_current_state(self):
        if not self.state_stack:
            self.reset_stack()
            return False
        return self.state_stack[-1]

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
        state = self.get_current_state()
        if state:
            state.on_update(elapsed)
        return

    def on_render(self, screen):
        " Called on render "
        state = self.get_current_state()
        if state:
            state.on_render(screen)
        return

    def on_key_down(self, key):
        state = self.get_current_state()
        if state:
            state.on_key_down(key)

    def on_mouse_event(self, pos):
        state = self.get_current_state()
        if state:
            state.on_mouse_event(pos)

    def on_mouse_motion(self, event, pos):
        state = self.get_current_state()
        if state:
            state.on_mouse_motion(event, pos)

    def on_mouse_down(self, event, pos):
        state = self.get_current_state()
        if state:
            state.on_mouse_down(event, pos)

    def on_mouse_up(self, event, pos):
        state = self.get_current_state()
        if state:
            state.on_mouse_up(event, pos)
