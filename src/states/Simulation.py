" Andy "
import pygame

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
from ..ml.agents import QLearn
from ..ml.environments import Maze as Environment

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.environment = Environment()
        self.agent = QLearn(2, 4, alpha=1)

        self.episode = 0
        self.tick_rate = 1
        self.total_time = 0
        self.render_time = 0
        self.total_reward = 0

        self.prev_state = self.environment.reset()

        self.human_action = -1

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
        self.environment.on_render(screen, self.agent.model.predict)

    def on_mouse_event(self, event):
        self.environment.on_mouse_event(event)

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            if self.tick_rate == 1000:
                self.tick_rate = 1
            elif self.tick_rate == 1:
                self.tick_rate = 0
            else:
                self.tick_rate = 1000
        elif key == pygame.K_y:
            if self.render_time == 60:
                self.render_time = 0
            else:
                self.render_time = 60
        elif key == pygame.K_LEFT:
            self.human_action = 2
        elif key == pygame.K_RIGHT:
            self.human_action = 1
        elif key == pygame.K_UP:
            self.human_action = 0
        elif key == pygame.K_DOWN:
            self.human_action = 3
