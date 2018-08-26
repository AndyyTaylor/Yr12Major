import pygame
import numpy as np
import random
from enum import Enum
from .config import *

class Actions(Enum):
    FORWARD = 0
    RIGHT = 1
    LEFT = 2
    BACK = 3

class MazeEnv():
    ''' TODO '''
    def __init__(self, GW, GH, SW, SH):
        global GRID_WIDTH, GRID_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, BOX_WIDTH, BOX_HEIGHT

        GRID_WIDTH = GW
        GRID_HEIGHT = GH
        SCREEN_WIDTH = SW
        SCREEN_HEIGHT = SH

        BOX_WIDTH = SCREEN_WIDTH/GRID_WIDTH
        BOX_HEIGHT = SCREEN_HEIGHT/GRID_HEIGHT

        WIN_STATE = random.randint(0, GRID_WIDTH * GRID_HEIGHT - 1)
        # Setup ML stuff
        self.pos = np.array(self.getPos(SPAWN_STATE))
        self.action_space = Actions
        self.max_states = GRID_WIDTH * GRID_HEIGHT
        self.max_actions = len(self.action_space)

        self.Q = np.zeros([GRID_WIDTH*GRID_HEIGHT, len(self.action_space)])

        self.tunnel_vision = False

        # Other
        self.WALLS = list(WALLS)
        self.WIN_STATE = WIN_STATE
        self.SPAWN_STATE = SPAWN_STATE

    def step(self, action):
        self.pos = self.moveDir(self.pos, self.action_space(action))

        reward = -0.04
        done = True
        if self.getState() == self.WIN_STATE:
            reward = 10
        else:
            done = False

        return (self.getState(), reward, done, {})

    def reset(self):
        self.pos = np.array(self.getPos(self.SPAWN_STATE))

    def render(self, screen, close=False):
        self.screen = screen
        self.screen.fill((0, 0, 0))

        # Draw the grid
        # font = pygame.font.Font(None, 22)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                all_points = []
                all_points.append([[x * BOX_WIDTH, y * BOX_HEIGHT], [x * BOX_WIDTH+BOX_WIDTH, y * BOX_HEIGHT], [x * BOX_WIDTH+BOX_WIDTH/2, y * BOX_HEIGHT+BOX_HEIGHT/2]])
                all_points.append([[x * BOX_WIDTH+BOX_WIDTH, y * BOX_HEIGHT], [x * BOX_WIDTH+BOX_WIDTH, y * BOX_HEIGHT+BOX_HEIGHT], [x * BOX_WIDTH+BOX_WIDTH/2, y * BOX_HEIGHT+BOX_HEIGHT/2]])
                all_points.append([[x * BOX_WIDTH, y * BOX_HEIGHT], [x * BOX_WIDTH, y * BOX_HEIGHT+BOX_HEIGHT], [x * BOX_WIDTH+BOX_WIDTH/2, y * BOX_HEIGHT+BOX_HEIGHT/2]])
                all_points.append([[x * BOX_WIDTH+BOX_WIDTH, y * BOX_HEIGHT+BOX_HEIGHT], [x * BOX_WIDTH, y * BOX_HEIGHT+BOX_HEIGHT], [x * BOX_WIDTH+BOX_WIDTH/2, y * BOX_HEIGHT+BOX_HEIGHT/2]])

                width = 34
                height = 10
                text_offs = [[(BOX_WIDTH/2-width/2), height/2], [BOX_WIDTH-width, BOX_HEIGHT/2-height/2], [4, BOX_HEIGHT/2-height/2], [BOX_WIDTH/2-width/2, BOX_HEIGHT-height-4]]

                for a in range(4):
                    s = pygame.Surface((BOX_WIDTH,BOX_HEIGHT), pygame.SRCALPHA)
                    s.fill((0, 0, 0, 0))

                    if self.getState((x, y)) == self.WIN_STATE:
                        col = (0, 255, 0, 255)
                    elif [x, y] in self.WALLS:
                        col = (128, 128, 128, 255)
                    elif len(self.Q) <= self.getState((x, y)) or len(self.Q[self.getState((x, y))]) <= a:
                        col = (0, 0, 0, 0)
                    elif self.Q[self.getState((x, y))][a] > 0:
                        col = (0, 255, 0, 60 + self.Q[self.getState((x, y))][a] / self.Q.max() * 195)
                    elif self.Q[self.getState((x, y))][a] < 0:
                        col = (255, 0, 0, 60 + self.Q[self.getState((x, y))][a] / self.Q.min() * 195)
                    else:
                        col = (0, 0, 0, 0)

                    if not self.tunnel_vision or self.getState((x, y)) == self.getState():
                        pygame.draw.polygon(s, col, [[all_points[a][b][0]-x*BOX_WIDTH, all_points[a][b][1]-y*BOX_HEIGHT] for b in range(3)])
                        self.screen.blit(s, (x*BOX_WIDTH, y*BOX_HEIGHT))

                        if self.getState((x, y)) != self.WIN_STATE and [x, y] not in self.WALLS:
                            pygame.draw.polygon(self.screen, (255, 255, 255), all_points[a], 2)

                            #if BOX_WIDTH > 80:
                                #trender = font.render("{0:.2f}".format(self.Q[self.getState((x, y)), a]), True, (255, 255, 255))
                                #self.screen.blit(trender, (x*BOX_WIDTH+text_offs[a][0], y*BOX_HEIGHT+text_offs[a][1]))

        # Draw the player
        pygame.draw.circle(self.screen, (0, 0, 255),
                          (int((self.pos[0]+0.5)*BOX_WIDTH),
                          int((self.pos[1]+0.5)*BOX_HEIGHT)),
                          max(10, int(BOX_WIDTH/10)))

        pygame.display.update()

    def moveDir(self, pos, action):
        oldPos = list(pos)
        if action == Actions.FORWARD:
            pos[1] -= 1
        elif action == Actions.RIGHT:
            pos[0] += 1
        elif action == Actions.LEFT:
            pos[0] -= 1
        elif action == Actions.BACK:
            pos[1] += 1

        if pos[0] < 0 or pos[0] >= GRID_WIDTH or pos[1] < 0 or pos[1] >= GRID_HEIGHT \
                      or self.hitWall(pos):
            pos = oldPos

        return pos

    def hitWall(self, pos):
        for w in self.WALLS:
            if w[0] == pos[0] and w[1] == pos[1]:
                return True
        return False

    def getState(self, pos=False):
        if not pos:
            pos = self.pos

        return int(pos[1]*GRID_WIDTH+pos[0])

    def getPos(self, state):
        return [state % GRID_WIDTH, state // GRID_WIDTH]