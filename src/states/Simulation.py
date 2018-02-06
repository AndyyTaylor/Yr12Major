" Andy "
import pygame

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
from ..ml.agents import DeepQNetwork as Agent
from ..ml.environments import MountainCar as Environment

class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.episode = 0
        self.total_time = 0
        self.total_reward = 0
        self.tick_rate = 100
        self.prev_reward = []

        self.environment = Environment()
        self.agent = Agent(self.environment.get_observation_space(), self.environment.get_action_space())

        self.obvs = self.environment.reset()
        self.reward = 0
        self.done = False

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self):
        self.environment.on_init()

    def on_exit(self):
        pass

    def on_update(self, elapsed):

        action = self.agent.choose_action(self.obvs)

        prev_obvs = self.obvs
        self.obvs, reward, done, _ = self.environment.step(action)
        reward += abs(self.obvs[0])
        # print((self.obvs[0] + 0.5) ** 2)
        self.agent.train(prev_obvs, self.obvs, action, reward, done)

        self.total_reward += reward

        if done:
            self.obvs = self.environment.reset()

            self.agent.reset()
            self.prev_reward.append(self.total_reward)

            if len(self.prev_reward) > 50:
                self.prev_reward.pop(0)

            print(self.episode, '..', self.total_reward)

            self.total_reward = 0
            self.episode += 1

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
