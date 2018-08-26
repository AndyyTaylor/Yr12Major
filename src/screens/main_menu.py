
import pygame
from src import config
from .screen import Screen
from ..widgets import *
from .maze.mazeenv import MazeEnv
from .maze.qlearn import QLearn
from time import time


class MainMenu(Screen):

    def __init__(self):
        super().__init__("MainMenu", "MasterState", show_title=False, back_button=False)

        self.widgets.append(Button(50, config.SCREEN_HEIGHT - 270, 400, 100, "Play",
                            64, config.BLACK, config.BLACK, config.SCHEME2, 6,
                            lambda: self.parent.change_state("LevelSelector")))

        self.widgets.append(Button(50, config.SCREEN_HEIGHT - 150, 400, 100, "Shop",
                            64, config.BLACK, config.BLACK, config.SCHEME2, 6,
                            lambda: self.parent.change_state("Shop")))

        self.maze = MazeEnv(config.MAZE_WIDTH, config.MAZE_HEIGHT,
                            config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.agent = QLearn(self.maze.max_actions)
        self.agent.reset(self.maze.getState())
        self.last_move = time()
        self.moved = True

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

        self.maze = MazeEnv(config.MAZE_WIDTH, config.MAZE_HEIGHT,
                            config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.agent = QLearn(self.maze.max_actions)
        self.agent.reset(self.maze.getState())
        self.last_move = time()

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if time() > self.last_move + max(1 - config.PURCHASES.count("Player Speed") * 0.05, 0.1):
            new_state, reward, done, obv = self.maze.step(self.agent.getAction())

            self.agent.update(new_state, reward)
            self.maze.Q = self.agent.Q

            if done:
                self.maze.reset()
                self.agent.reset(self.maze.getState())

            self.moved = True
            self.last_move = time()

    def on_render(self, screen, back_fill=None):
        if self.moved:
            self.maze.render(screen)

            pygame.draw.rect(screen, config.SCHEME5, (0, config.SCREEN_HEIGHT / 3 * 2, config.SCREEN_WIDTH / 3, config.SCREEN_HEIGHT / 3))

            for widget in self.widgets:
                widget.changed = True

            self.moved = False

        super().on_render(screen)

