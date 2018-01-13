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

        StateRegistry.instance().register_group(self)
        if parent:
            self.parent = StateRegistry.instance().get_group(parent)
            self.parent.add_child(self)
        elif name != "MasterState":
            self.parent = StateRegistry.instance().get_group("MasterState")
            self.parent.add_child(self)

        print("created")

    def add_child(self, child):
        self.children[child.name] = child

    def change_state(self, name):
        if self.state_stack:
            self.state_stack.pop().on_exit()

        self.state_stack = []

        if name in self.children:
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
        print("Resetting Stack")
        for key, val in self.children.items():
            print("Set stack to " + key)
            self.state_stack.append(val)
            return

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

    def on_render(self):
        " Called on render "
        return
