" Andy "
import pygame

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
from ..ml.agents import QLearn
from ..ml.environments import CatchApples as Environment

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.agent = QLearn(4, 3)
        self.environment = Environment()

        self.episode = 0
        self.tick_rate = 1
        self.total_time = 0
        self.render_time = 0
        self.total_reward = 0

        self.prev_state = self.environment.reset()

    def on_init(self):
        pass

    def on_shutdown(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        self.total_time += elapsed
        if self.total_time < self.render_time:
            return

        self.total_time = 0

        for tick in range(self.tick_rate):
            action = self.agent.choose_action(self.prev_state)
            new_state, reward, done, _ = self.environment.step(action)

            self.agent.train(self.prev_state, action, reward, done, new_state)

            self.prev_state = new_state
            self.total_reward += reward

            if done:
                self.agent.reset()
                self.prev_state = self.environment.reset()

                print('Episode', self.episode, '..', self.total_reward)

                self.episode += 1
                self.total_reward = 0

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_down(self, pos):
        pass

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            if self.tick_rate == 1000:
                self.tick_rate = 1
            else:
                self.tick_rate = 1000
        elif key == pygame.K_y:
            if self.render_time == 60:
                self.render_time = 0
            else:
                self.render_time = 60
        elif key == pygame.K_l:
            self.agent.only_optimal(True)
        elif key == pygame.K_r:
            self.agent.only_optimal(False)
