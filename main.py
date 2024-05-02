import pygame
from background import Background
from player import Player
from zombie import ZombieManager
from projectile import ProjectileManager
from gravestone import GravestoneManager
from shop import Shop
from weapon import Weapon
import start_screen
import death_screen

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

START_SCREEN = 0
GAME = 1
RESTART_SCREEN = 2

state = START_SCREEN


def start():
    global state
    state = GAME


def draw():
    offset = (player.x_pos - WIDTH // 2, player.y_pos - HEIGHT // 2)
    bg.draw(screen, *offset)
    graves.draw(screen, *offset)
    player.draw(screen)
    zombies.draw(screen, *offset)
    projectiles.draw(screen, *offset)
    bg.draw_hedges(screen, *offset)
    Shop.draw_ui()


def reset():
    global state
    state = GAME
    # todo: call reset functions everywhere
    Shop.init(screen)
    Weapon.reset()
    player.reset()
    projectiles.reset()
    zombies.reset()
    graves.reset()


start_screen.init(start, screen)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if state == START_SCREEN:
        start_screen.step()
    elif state == GAME:
        draw()
        if not Shop.is_open:
            Shop.tick()
            player.update()
            zombies.update(player)
            projectiles.update(zombies)
            graves.update()
            if player.health <= 0:
                death_screen.init(reset, screen)
                state = RESTART_SCREEN
        else:
            Shop.update_shop()
            Shop.draw_shop(screen)
    elif state == RESTART_SCREEN:
        death_screen.step()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
