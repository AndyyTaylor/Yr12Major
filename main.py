" Andy "
import pygame
import src.config as config
from src.framework.StateRegistry import StateRegistry
from src.framework.stategroups.StateGroup import StateGroup

pygame.init()

SCREEN = pygame.display.set_mode((600, 600), 0, 32)


REGISTERY = StateRegistry.instance()
P = StateGroup()


RUNNING = True
while RUNNING:
    SCREEN.fill(config.WHITE)

    REGISTERY.get_state("name")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    pygame.display.update()
