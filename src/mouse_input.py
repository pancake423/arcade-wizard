import pygame
OFFSET, SCALE = ((0, 0), 0)


def init(offset, scale):
    global OFFSET
    global SCALE
    OFFSET, SCALE = offset, scale


def get_pos():
    x, y = pygame.mouse.get_pos()
    return (x - OFFSET[0]) / SCALE, (y - OFFSET[1]) / SCALE
