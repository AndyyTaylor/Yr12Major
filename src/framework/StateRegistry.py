" doc "


class StateRegistry():
    _instance = None

    def __init__(self):
        self.all_states = {}
        self.all_groups = {}
        self.state_stack = []
        self.data_stack = []

    def register(self, state, parent_name):
        self.all_states[state.name] = state
        parent = self.get_group(parent_name)
        if parent:
            parent.add_child(state)
        return parent

    def register_group(self, state_group):
        self.all_groups[state_group.name] = state_group

    def get_state(self, name):
        if name in self.all_states:
            return self.all_states[name]

        return False

    def get_group(self, name):
        if name in self.all_groups:
            return self.all_groups[name]

        return False

    def push_stack(self, data):
        self.data_stack.append(data)

    def pop_stack(self):
        return self.data_stack.pop(), self.screen

    def set_screen(self, screen):
        self.screen = screen

    @staticmethod
    def instance():
        if not StateRegistry._instance:
            StateRegistry._instance = StateRegistry()

        return StateRegistry._instance
