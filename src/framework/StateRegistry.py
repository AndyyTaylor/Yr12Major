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

    @staticmethod
    def instance():
        if not StateRegistry._instance:
            StateRegistry._instance = StateRegistry()

        return StateRegistry._instance
