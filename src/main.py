" Andy "
import pygame
import config

pygame.init()

SCREEN = pygame.display.set_mode((600, 600), 0, 32)


RUNNING = True
while RUNNING:
    SCREEN.fill(config.WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    pygame.display.update()
