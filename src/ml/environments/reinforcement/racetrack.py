import random
import pygame
import math
import numpy as np

from .... import config

class RaceTrack():
    def __init__(self):
        self.num_observations = 2
        self.num_actions = 3

        self.track_points = []
        self.track_width = 60

        self.car_pos = [0, 0]
        self.car_angle = 1
        self.car_speed = 5
        self.car_width = 10

        self.start_pos = [0, 0]
        self.start_angle = 1

        self.mouse_down = False

    def step(self, action):
        reward = 0.05
        done = False

        self.car_pos[0] += math.cos(self.car_angle) * self.car_speed
        self.car_pos[1] += math.sin(self.car_angle) * self.car_speed

        if not self.is_on_track(tuple(self.car_pos)):
            done = True
            reward = -1

        return self.get_state(), reward, done, {}

    def reset(self):
        self.car_pos = list(self.start_pos)
        self.car_angle = self.start_angle

        return self.get_state()

    def on_render(self, screen, predict):
        screen.fill(config.BLACK)

        for point in self.track_points:
            pygame.draw.circle(screen, config.GRAY, point, int(self.track_width/2))

        orig_points = [[self.start_pos[0] - self.track_width/2, self.start_pos[1] - 5],
                       [self.start_pos[0] - self.track_width/2, self.start_pos[1] + 5],
                       [self.start_pos[0] + self.track_width/2, self.start_pos[1] + 5],
                       [self.start_pos[0] + self.track_width/2, self.start_pos[1] - 5]]

        points = [list(self.rotate(tuple(self.start_pos), tuple(point), self.start_angle - math.radians(90))) for point in orig_points]
        pygame.draw.polygon(screen, config.RED, points)

        orig_points = [[self.car_pos[0] - self.car_width/2, self.car_pos[1] - 5],
                       [self.car_pos[0] - self.car_width/2, self.car_pos[1] + 5],
                       [self.car_pos[0] + self.car_width/2, self.car_pos[1] + 5],
                       [self.car_pos[0] + self.car_width/2, self.car_pos[1] - 5]]

        points = [list(self.rotate(tuple(self.car_pos), tuple(point), self.car_angle)) for point in orig_points]
        pygame.draw.polygon(screen, config.BLUE, points)

    def get_state(self):
        return [0, 0]   # TODO

    def is_on_track(self, pos):
        x, y = pos
        for point in self.track_points:
            x2 = point[0]
            y2 = point[1]

            if self.distance(x, y, x2, y2) < self.track_width/2:
                return True

        return False

    def on_mouse_event(self, event):
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_down = True
                self.track_points.append(pos)
            elif event.button == 3:
                if self.start_angle:
                    self.start_pos = pos
                    self.start_angle = False
                else:
                    self.start_angle = math.atan2(pos[1]-self.start_pos[1], pos[0]-self.start_pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
            elif event.button == 3:
                pass
        elif event.type == pygame.MOUSEMOTION and self.mouse_down:
            self.track_points.append(pos)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def rotate(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

