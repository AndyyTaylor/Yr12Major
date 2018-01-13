" doc "

from ..StateRegistry import StateRegistry

class StateGroup():
    " doc "

    def __init__(self):
        self.state_stack = []
        print("created")

    def change_state(self, name):
        if self.state_stack:
            self.state_stack.pop().on_exit()

        self.state_stack = []

        state = StateRegistry.instance().get_state(name)     # Registry get state
        state.on_enter()

        self.state_stack.append(state)

    def push_state(self, new_state):
        state = StateRegistry.instance().get_state(new_state)
        state.on_enter()

        self.state_stack.append(state)

    def pop_state(self):
        if self.state_stack:
            self.state_stack.pop().on_exit()
