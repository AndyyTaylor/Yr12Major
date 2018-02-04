" Andy "
import pygame

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
from ..ml.agents import QLearn as Agent
from ..ml.environments import Pendulum as Environment

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.total_time = 0
        self.total_reward = 0
        self.tick_rate = 100
        self.prev_reward = []

        self.environment = Environment()
        self.agent = Agent(self.environment.num_actions)

        self.obvs = self.environment.reset()

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        self.environment.on_init()

    def on_exit(self):
        pass

    def on_update(self, elapsed):
        self.total_time += elapsed

        if self.total_time > self.tick_rate:
            self.total_time = 0

            action = self.agent.get_action(self.obvs)
            self.obvs, reward, done, info = self.environment.step(action)
            self.agent.update(self.obvs, reward)
            self.total_reward += reward

            if done:
                self.agent.reset(self.environment.reset())
                self.prev_reward.append(self.total_reward)
                if len(self.prev_reward) > 50:
                    self.prev_reward.pop(0)
                print(self.agent.episodes, "-", self.total_reward, sum(self.prev_reward)/len(self.prev_reward))
                self.total_reward = 0

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_down(self, pos):
        self.environment.on_mouse_down(pos)

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            if self.tick_rate == 100:
                self.tick_rate = 0
            else:
                self.tick_rate = 100
        self.environment.on_key_down(key)
