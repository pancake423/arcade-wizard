import pygame
from background import Background
from player import Player

WIDTH, HEIGHT = 1200, 800

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("CS 353 Final Project")

bg = Background()
player = Player(WIDTH, HEIGHT, Background.width, Background.height)


def draw():
    bg.draw(screen, player.x_pos - WIDTH // 2, player.y_pos - HEIGHT // 2)
    player.draw(screen)
    bg.draw_hedges(screen, player.x_pos - WIDTH // 2, player.y_pos - HEIGHT // 2)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()
    draw()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
