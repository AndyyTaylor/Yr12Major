import pygame
import random
import numpy as np

from .... import config


class GridWorld():

    def __init__(self):
        self.WIDTH = 4
        self.HEIGHT = 3

        self.num_observations = 2
        self.num_actions = 4

        self.step_cost = -0.5

        self.player_pos = (0, 2)
        self.wall_pos = [(1, 1)]
        self.win_pos = [(3, 0)]
        self.lose_pos = [(3, 1)]

    def step(self, action):
        move_dir = self.get_move_dir(action)
        reward, done = self.move_player(move_dir)

        return (self.get_obvs(), reward, done, {})

    def on_render(self, screen, get_val):
        box_width = screen.get_width() / self.WIDTH
        box_height = screen.get_height() / self.HEIGHT

        for xx in range(self.WIDTH):
            for yy in range(self.HEIGHT):
                color = self.get_tile_col((xx, yy), get_val)

                pygame.draw.rect(screen, color, (box_width * xx, box_height * yy, box_width, box_height))
                pygame.draw.rect(screen, config.WHITE, (box_width * xx, box_height * yy, box_width, box_height), 5)

                if (xx, yy) == self.player_pos:
                    pygame.draw.circle(screen, config.BLUE, (int(box_width * xx + box_width/2), int(box_height * yy + box_height/2)), 10)

    def get_tile_col(self, tile, get_val):
        tile_val = get_val(np.array(tile))

        color = config.BLACK
        if tile in self.win_pos:
            color = config.GREEN
        elif tile in self.lose_pos:
            color = config.RED
        elif tile in self.wall_pos:
            color = config.GRAY
        elif tile_val > 0:
            color = (0, int(tile_val * 255), 0)
        elif tile_val < 0:
            color = (min(int(-tile_val * 255), 255), 0, 0)

        return color

    def move_player(self, move_dir):
        new_pos = tuple(map(sum, zip(self.player_pos, move_dir)))

        if new_pos in self.wall_pos or new_pos[0] < 0 or new_pos[0] >= self.WIDTH \
                or new_pos[1] < 0 or new_pos[1] >= self.HEIGHT:
            return self.step_cost, False

        self.player_pos = new_pos

        if new_pos in self.win_pos:
            return 1, True

        if new_pos in self.lose_pos:
            return -1, True

        return self.step_cost, False

    def get_move_dir(self, action):
        if action == 0:
            move_dir = (0, -1)
        elif action == 1:
            move_dir = (1, 0)
        elif action == 2:
            move_dir = (0, 1)
        elif action == 3:
            move_dir = (-1, 0)
        else:
            raise LookupError("Invalid Action: " + str(action))

        return move_dir

    def reset(self):
        self.player_pos = (0, 2)

        return self.get_obvs()

    def get_state_if_move(self, action):
        old_pos = self.player_pos
        obvs, reward, done, _ = self.step(action)
        self.player_pos = old_pos

        return obvs

    def on_mouse_event(self, event):
        pass

    def get_obvs(self):
        return np.array(self.player_pos)

    def sample_action(self):
        return random.randint(0, self.num_actions-1)
