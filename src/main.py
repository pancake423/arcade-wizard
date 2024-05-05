import pygame
from src.background import Background
from src.player import Player
from src.zombie import ZombieManager
from src.projectile import ProjectileManager
from src.gravestone import GravestoneManager
from src.shop import Shop
from src.weapon import Weapon
from src.label import Label
import src.start_screen as start_screen
import src.death_screen as death_screen
import src.pause_menu as pause_menu

pygame.init()

WIDTH, HEIGHT = 1200, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Wizard Arcade")
pygame_icon = pygame.image.load('src/wizard-head.png')
pygame.display.set_icon(pygame_icon)

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
new_state = START_SCREEN
fade_timer = 0
fade_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


def start():
    global new_state
    global fade_timer
    new_state = GAME
    fade_timer = 120


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
    global new_state
    new_state = GAME
    global fade_timer
    fade_timer = 120
    # todo: call reset functions everywhere
    Shop.init(screen)
    Weapon.reset()
    player.reset()
    projectiles.reset()
    zombies.reset()
    graves.reset()


start_screen.init(start, screen)
pause_menu.init(screen)

# Main loop
running = True
paused = False
def main():
    global state
    global running
    global paused
    global fade_timer
    global new_state
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.ACTIVEEVENT and state == GAME:
                if event.state != 1:  # event.gain != 1 or
                    paused = True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                paused = False if paused else True
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                Shop.toggle()
        if state == START_SCREEN:
            start_screen.step()
        elif state == GAME and fade_timer < 60:
            draw()
            if paused:
                if Shop.is_open:
                    Shop.draw_shop(screen)
                pause_menu.draw()
            else:
                if not Shop.is_open:
                    Shop.tick()
                    player.update()
                    zombies.update(player)
                    projectiles.update(zombies)
                    graves.update()
                    if player.health <= 0:
                        death_screen.init(reset, screen, Shop.time_alive)
                        new_state = RESTART_SCREEN
                        fade_timer = 120
                else:
                    Shop.update_shop()
                    Shop.draw_shop(screen)
        elif state == RESTART_SCREEN:
            death_screen.step()

        if fade_timer > 0:
            if fade_timer > 60:
                fade_surf.fill((0, 0, 0, 255 - 255 * ((fade_timer-60) / 60)))
            else:
                fade_surf.fill((0, 0, 0, 255 * (fade_timer / 60)))
            screen.blit(fade_surf, (0, 0))
            fade_timer -= 1
            if fade_timer == 60:
                state = new_state

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
