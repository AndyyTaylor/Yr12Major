import pygame
import numpy as np

GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOX_WIDTH = SCREEN_WIDTH/GRID_WIDTH
BOX_HEIGHT = SCREEN_HEIGHT/GRID_HEIGHT
WIN_STATE = 3
LOSE_STATE = 5
SPAWN_STATE = 6
WALLS = [[0, 0]]

class Maze():
    ''' TODO '''
    def __init__(self):
        # Setup ML stuff
        self.pos = np.array(self.getPos(SPAWN_STATE))
        self.num_actions = 4
        self.max_states = GRID_WIDTH * GRID_HEIGHT

        self.Q = np.zeros([GRID_WIDTH*GRID_HEIGHT, self.num_actions])

        self.tunnel_vision = False

        # Other
        self.WALLS = list(WALLS)
        self.WIN_STATE = WIN_STATE
        self.LOSE_STATE = LOSE_STATE
        self.SPAWN_STATE = SPAWN_STATE

    def step(self, action):
        self.pos = self.moveDir(self.pos, action)

        reward = -0.04
        done = True
        if self.getState() == self.WIN_STATE:
            reward = 10
        elif self.getState() == self.LOSE_STATE:
            reward = -10
        else:
            done = False

        return (list(self.pos), reward, done, {})

    def reset(self):
        self.pos = np.array(self.getPos(self.SPAWN_STATE))
        return list(self.pos)

    def on_render(self, screen, predict):
        screen.fill((0, 0, 0))

        self.Q = np.zeros([GRID_WIDTH*GRID_HEIGHT, self.num_actions])
        for xx in range(GRID_WIDTH):
            for yy in range(GRID_HEIGHT):
                self.Q[self.getState([xx, yy])] = predict([xx, yy])

        # Draw the grid
        #font = pygame.font.Font(None, 22)
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
                    elif self.getState((x, y)) == self.LOSE_STATE:
                        col = (255, 0, 0, 255)
                    elif [x, y] in self.WALLS:
                        col = (128, 128, 128, 255)
                    elif self.Q[self.getState((x, y))][a] > 0:
                        col = (0, 255, 0, 60 + self.Q[self.getState((x, y))][a] / self.Q.max() * 195)
                    elif self.Q[self.getState((x, y))][a] < 0:
                        col = (255, 0, 0, 60 + self.Q[self.getState((x, y))][a] / self.Q.min() * 195)
                    else:
                        col = (0, 0, 0, 0)

                    if not self.tunnel_vision or self.getState((x, y)) == self.getState():
                        pygame.draw.polygon(s, col, [[all_points[a][b][0]-x*BOX_WIDTH, all_points[a][b][1]-y*BOX_HEIGHT] for b in range(3)])
                        screen.blit(s, (x*BOX_WIDTH, y*BOX_HEIGHT))

                        if self.getState((x, y)) != self.WIN_STATE and self.getState((x, y)) != self.LOSE_STATE and [x, y] not in self.WALLS:
                            pygame.draw.polygon(screen, (255, 255, 255), all_points[a], 2)

                            #if BOX_WIDTH > 80:
                                #trender = font.render("{0:.2f}".format(self.Q[self.getState((x, y)), a]), True, (255, 255, 255))
                                #screen.blit(trender, (x*BOX_WIDTH+text_offs[a][0], y*BOX_HEIGHT+text_offs[a][1]))

        # Draw the player
        pygame.draw.circle(screen, (0, 0, 255),
                          (int((self.pos[0]+0.5)*BOX_WIDTH),
                          int((self.pos[1]+0.5)*BOX_HEIGHT)),
                          max(10, int(BOX_WIDTH/10)))

        pygame.display.update()

    def moveDir(self, pos, action):
        oldPos = list(pos)
        if action == 0:
            pos[1] -= 1
        elif action == 1:
            pos[0] += 1
        elif action == 2:
            pos[0] -= 1
        elif action == 3:
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

    def on_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = list(pygame.mouse.get_pos())
            pos = [int(x) for x in pos]
            pos[0] = pos[0] // int(BOX_WIDTH)
            pos[1] = pos[1] // int(BOX_HEIGHT)
            self.clicked_state = self.getState(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = list(pygame.mouse.get_pos())
            pos = [int(x) for x in pos]
            pos[0] = pos[0] // int(BOX_WIDTH)
            pos[1] = pos[1] // int(BOX_HEIGHT)
            self.up_state = self.getState(pos)

            if self.clicked_state == self.WIN_STATE:
                self.WIN_STATE = self.up_state
            elif self.clicked_state == self.LOSE_STATE:
                self.LOSE_STATE = self.up_state
            elif self.clicked_state == self.SPAWN_STATE:
                self.SPAWN_STATE = int(self.up_state)
            elif self.up_state == self.clicked_state:
                if pos not in self.WALLS:
                    self.WALLS.append(pos)
                else:
                    self.WALLS.remove(pos)
