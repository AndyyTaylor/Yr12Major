import random
import os
import struct
import pygame
import numpy as np

from .... import config
from ....states.AbstractState import State
from ....ui.DataImage import DataImage
from ....ui.Textbox import Textbox
from ....ui.Button import Button


class TicTacToe(State):
    " The main state for this enviroment "

    def __init__(self):
        super().__init__("Catch Apples", "Environments")

        self.num_observations = 9
        self.num_actions = 9

        self.reward = 0

        self.num_rows = 3
        self.num_columns = 3

        self.x = 1
        self.y = -1
        self.sym = self.x

        self.board = np.zeros((self.num_rows, self.num_columns))

    def reset(self):
        self.board = np.zeros((self.num_rows, self.num_columns))

        return self.get_obvs()

    def step(self, action):
        reward = 0

        valid = self.take_action(action)

        done = True
        if self.check_winning(-1):
            reward = -1
        elif self.check_winning(1):
            reward = 1
        elif np.count_nonzero(self.board) == self.num_rows * self.num_columns:
            reward = 0
        else:
            done = False

        if done:
            self.sym = self.x

        return (self.get_obvs(), reward, done, {'valid': valid})

    def get_obvs(self):
        return self.board.flatten()

    def take_action(self, action, val=-2):
        if val == -2:
            val = self.sym

        row = action // self.num_rows
        column = action % self.num_rows

        if self.board[row, column] == 0 or val == 0:
            self.board[row, column] = val
            if self.sym == self.x:
                self.sym = self.y
            else:
                self.sym = self.x
            return True

        return False

    def check_winning(self, val):
        for rr in range(self.num_rows):
            won = True

            for cc in range(self.num_columns):
                if self.board[rr, cc] != val:
                    won = False
                    break

            if won:
                return True

        for cc in range(self.num_columns):
            won = True

            for rr in range(self.num_rows):
                if self.board[rr, cc] != val:
                    won = False
                    break

            if won:
                return True

        won = True
        for i in range(3):
            if self.board[i, i] != val:
                won = False
                break

        if won:
            return True

        won = True
        for i in range(3):
            if self.board[self.num_rows-1-i, i] != val:
                won = False
                break

        if won:
            return True

        return False

    def on_render(self, screen, predict, _=None):
        pygame.draw.rect(screen, config.BLACK, (180, 20, 20, 560))
        pygame.draw.rect(screen, config.BLACK, (400, 20, 20, 560))
        pygame.draw.rect(screen, config.BLACK, (20, 180, 560, 20))
        pygame.draw.rect(screen, config.BLACK, (20, 400, 560, 20))

        for rr in range(self.num_rows):
            for cc in range(self.num_columns):
                s = self.get_state_if_move(rr * self.num_rows + cc)
                if np.any(s != self.get_obvs()):
                    acc = predict(s, env=self)
                    if acc > 0:
                        pygame.draw.rect(screen, (0, acc * 255, 0), (50 + cc * 200, 50 + rr * 200, 100, 100))
                    else:
                        pygame.draw.rect(screen, (-acc * 255, 0, 0), (50 + cc * 200, 50 + rr * 200, 100, 100))

                val = self.board[rr, cc]
                if val == -1:
                    self.draw_O(screen, 100 + cc * 200, 100 + rr * 200)
                elif val == 1:
                    self.draw_X(screen, 100 + cc * 200, 100 + rr * 200)

    def draw_O(self, screen, x, y):
        pygame.draw.circle(screen, config.BLUE, (x, y), 70, 20)

    def draw_X(self, screen, x, y):
        pygame.draw.circle(screen, config.RED, (x, y), 70, 20)

    def on_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cc = pos[0] // 200
            rr = pos[1] // 200
            return self.take_action(rr * self.num_rows + cc)

    def get_state_if_move(self, action, val=-2):
        if val == -2:
            val = self.sym

        valid = self.take_action(action, val)
        obvs = self.get_obvs()
        if valid:
            self.take_action(action, 0)

        return obvs

    def make_winning_move(self, val, player=0):
        if player == 0:
            player = val

        for rr in range(self.num_rows):
            missing = -1

            for cc in range(self.num_columns):
                if self.board[rr, cc] != val:
                    if missing != -1:
                        missing = -1
                        break
                    else:
                        missing = cc

            if missing != -1 and self.board[rr, missing] == 0:
                self.board[rr, missing] = player
                return True

        for cc in range(self.num_columns):
            missing = -1

            for rr in range(self.num_rows):
                if self.board[rr, cc] != val:
                    if missing != -1:
                        missing = -1
                        break
                    else:
                        missing = rr

            if missing != -1 and self.board[missing, cc] == 0:
                self.board[missing, cc] = player
                return True

        missing = -1
        for i in range(3):
            if self.board[i, i] != val:
                if missing != -1:
                    missing = -1
                    break
                else:
                    missing = i

        if missing != -1 and self.board[missing, missing] == 0:
            self.board[missing, missing] = player
            return True

        missing = -1
        for i in range(3):
            if self.board[self.num_rows-1-i, i] != val:
                if missing != -1:
                    missing = -1
                    break
                else:
                    missing = i

        if missing != -1 and self.board[self.num_rows-1-missing, missing] == 0:
            self.board[self.num_rows-1-missing, missing] = player
            return True

        return False

    def sample_action(self):
        r = [i for i in range(self.num_actions)]
        random.shuffle(r)

        for i in range(len(r)):
            if not self.take_action(r[i]):
                r[i] = r[min(i+1, len(r)-2)]
            else:
                self.take_action(r[i], 0)
                return r[i]
