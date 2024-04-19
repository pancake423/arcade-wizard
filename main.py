import pygame
from background import Background

WIDTH, HEIGHT = 800, 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("CS 353 Final Project")

bg = Background()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bg.draw(screen, WIDTH//-2, HEIGHT//-2)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
