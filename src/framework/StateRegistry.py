" doc "
import sys
sys.path.append("/Users/andytaylor/Google Drive/Major/src/framework/states")

class StateRegistry():
    _instance = None

    def __init__(self):
        self.all_states = {}
        self.state_stack = []
        print("created")

    def register(self, state):
        self.all_states[state.name] = state

    def get_state(self, name):
        if name in self.all_states:
            return self.all_states[name]

        return False

    def change_state(self, name):
        if self.state_stack:
            self.state_stack.pop().on_exit()

        self.state_stack = []

        state = self.get_state(name)
        state.on_enter()

        self.state_stack.append(state)

    @staticmethod
    def get_instance():
        if not StateRegistry._instance:
            StateRegistry._instance = StateRegistry()

        return StateRegistry._instance
