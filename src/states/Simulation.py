" Andy "
import pygame, random
import numpy as np

from .AbstractState import State

# from ..ml.environments import ClassPlot as Environment
# from ..ml.agents import NN as Agent
# from ..ml.environments import MNIST as Environment
# from ..ml.agents import LinearRegression as Agent
from ..ml.agents.deeplearning.layers import Dense
from ..ml.agents import QLearn as Agent
# from ..ml.environments import MNIST as Environment
from ..ml.environments import TicTacToe as Environment
from ..ml.agents.deeplearning.loss_functions import SquareLoss


class Simulation(State):
    " A "

    def __init__(self):
        super().__init__("Simulation", "MasterState")

        self.episode = 0
        self.total_time = 0
        self.render_time = 0
        self.total_reward = 0

        self.environment = Environment()
        self.agent = Agent(self.environment.num_observations, self.environment.num_actions)

        self.prev_state = self.environment.reset()
        self.reward = 0
        self.done = False

        self.tick_rate = 1

        self.prev_reward = []

        self.human_turn = True
        self.auto_turns = False

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
        if self.total_time < 0:
            return

        self.total_time = 0

        for tick in range(self.tick_rate):
            if self.human_turn and not self.auto_turns:
                break

            action = self.agent.choose_action(self.prev_state)
            new_state, reward, done, _ = self.environment.step(action)

            if _['valid'] and not done:
                if self.auto_turns:
                    self.human_turn = False

                    if random.random() < 0.5 or not self.environment.make_winning_move(-1):
                        if random.random() < 0.5 or not self.environment.make_winning_move(1, -1):
                            while not self.environment.take_action(random.randint(0, 8), -1):
                                pass
                else:
                    self.human_turn = True

            new_state = self.environment.get_obvs()

            self.agent.train(self.prev_state, action, reward, done, new_state)

            self.prev_state = new_state
            self.total_reward += reward

            if done:
                self.prev_state = self.environment.reset()

                print('Episode', self.episode, '..', self.total_reward)

                self.episode += 1
                self.total_reward = 0

    def on_render(self, screen):
        self.environment.on_render(screen)

    def on_mouse_event(self, event):
        if not self.human_turn:
            return

        valid = self.environment.on_mouse_event(event)
        if valid:
            self.human_turn = False

    def on_key_down(self, key):
        if key == pygame.K_SPACE:
            self.auto_turns = not self.auto_turns
