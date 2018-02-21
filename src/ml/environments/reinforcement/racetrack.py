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
        self.car_turn_speed = 5
        self.car_width = 10

        self.start_pos = [0, 0]
        self.start_angle = 1
        self.ticks = 0

        self.mouse_down = False

    def step(self, action):
        self.ticks += 1
        reward = 0.05
        done = False

        if action == 1:
            self.car_angle += math.radians(self.car_turn_speed)
        elif action == 2:
            self.car_angle -= math.radians(self.car_turn_speed)

        self.car_pos[0] += math.cos(self.car_angle) * self.car_speed
        self.car_pos[1] += math.sin(self.car_angle) * self.car_speed

        reward = np.sum(np.power(self.get_state(), 2))

        if not self.is_on_track(tuple(self.car_pos)):
            reward = -1
            done = True


        return self.get_state(), reward, done, {}

    def reset(self):
        self.ticks = 0
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

        collision_points = self.read_sensors(True)
        startX, startY = collision_points[0]

        for i in range(len(collision_points) - 1):
            x, y = collision_points[i + 1]
            pygame.draw.line(screen, config.RED, (startX, startY), (x, y))

    def get_state(self):
        fl = 0
        fr = 0

        fl, fr = self.read_sensors()

        return np.array([fl, fr])

    def read_sensors(self, render=False):
        startX = self.car_pos[0]
        startY = self.car_pos[1]

        collision_points = [(startX, startY)]

        x = startX
        y = startY
        while self.is_on_track((x, y)) and self.distance(startX, startY, x, y) < self.track_width:
            x += math.cos(math.radians(-45) + self.car_angle) * 3
            y += math.sin(math.radians(-45) + self.car_angle) * 3
        collision_points.append((x, y))
        fl = self.distance(startX, startY, x, y) / self.track_width

        x = startX
        y = startY
        while self.is_on_track((x, y)) and self.distance(startX, startY, x, y) < self.track_width:
            x += math.cos(math.radians(45) + self.car_angle) * 3
            y += math.sin(math.radians(45) + self.car_angle) * 3
        collision_points.append((x, y))
        fr = self.distance(startX, startY, x, y) / self.track_width

        if not render:
            return (fl, fr)
        return collision_points

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

