" Andy "
import sys
sys.path.append("/Users/andytaylor/Google Drive/Major/src/framework/")
sys.path.append("/Users/andytaylor/Google Drive/Major/src/framework/states")
sys.path.append("/Users/andytaylor/Google Drive/Major/src/framework/stategroups")

import pygame
import config
from IntroState import IntroState
from StateRegistry import StateRegistry

pygame.init()

SCREEN = pygame.display.set_mode((600, 600), 0, 32)


REGISTERY = StateRegistry.get_instance()


RUNNING = True
while RUNNING:
    SCREEN.fill(config.WHITE)

    REGISTERY.get_state("name")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    pygame.display.update()
