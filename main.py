import pygame
from sprite import Sprite

WIDTH, HEIGHT = 800, 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("CS 353 Final Project")

test = Sprite("wizard.png", WIDTH//2, HEIGHT//2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    test.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
