import pygame
from background import Background
from player import Player
from zombie import ZombieManager
from projectile import ProjectileManager
from gravestone import GravestoneManager
from shop import Shop

pygame.init()

WIDTH, HEIGHT = 1200, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("CS 353 Final Project")

bg = Background()
zombies = ZombieManager()
projectiles = ProjectileManager((Background.width, Background.height))
graves = GravestoneManager(zombies)
player = Player(WIDTH, HEIGHT, Background.width, Background.height, projectiles)
Shop.init(screen)


def draw():
    offset = (player.x_pos - WIDTH // 2, player.y_pos - HEIGHT // 2)
    bg.draw(screen, *offset)
    graves.draw(screen, *offset)
    player.draw(screen)
    zombies.draw(screen, *offset)
    projectiles.draw(screen, *offset)
    bg.draw_hedges(screen, *offset)
    Shop.draw_ui()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw()
    if not Shop.is_open:
        Shop.tick()
        player.update()
        zombies.update(player)
        projectiles.update(zombies)
        graves.update()
    else:
        Shop.update_shop()
        Shop.draw_shop(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
