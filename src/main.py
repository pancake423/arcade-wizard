import pygame
from src.background import Background
from src.player import Player
from src.zombie import ZombieManager
from src.projectile import ProjectileManager
from src.gravestone import GravestoneManager
from src.shop import Shop
from src.config import Weapon, Images
import src.start_screen as start_screen
import src.death_screen as death_screen
import src.pause_menu as pause_menu
import src.mouse_input as mouse_input
from src.button import Button

pygame.init()

WIDTH, HEIGHT = 1200, 800
OUT_WIDTH, OUT_HEIGHT = pygame.display.get_desktop_sizes()[0]
SCALE_FACTOR = min(OUT_WIDTH / WIDTH, OUT_HEIGHT / HEIGHT)
OFFSET = ((OUT_WIDTH - WIDTH * SCALE_FACTOR) // 2, (OUT_HEIGHT - HEIGHT * SCALE_FACTOR) // 2)

final_scaled = pygame.display.set_mode((OUT_WIDTH, OUT_HEIGHT), pygame.FULLSCREEN)
screen = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Wizard Arcade")
pygame_icon = pygame.image.load(Images.wizard_head)
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



def quit_loop():
    global running
    running = False


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
mouse_input.init(OFFSET, SCALE_FACTOR)
quit_button = Button(WIDTH - 100, HEIGHT - 63, 150, 75, "Quit",
                     callback=quit_loop, textcolor="white", color=(249, 53, 90), color_hover=(251, 114, 138))

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
            if event.type == pygame.KEYUP and event.key == pygame.K_e and state == GAME:
                Shop.toggle()
        if state == START_SCREEN:
            start_screen.step()
            quit_button.update()
            quit_button.draw(screen)
        elif state == GAME and fade_timer < 60:
            draw()
            if paused:
                if Shop.is_open:
                    Shop.draw_shop(screen)
                pause_menu.draw()
                quit_button.update()
                quit_button.draw(screen)
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
            quit_button.update()
            quit_button.draw(screen)

        if fade_timer > 0:
            if fade_timer > 60:
                fade_surf.fill((0, 0, 0, 255 - 255 * ((fade_timer-60) / 60)))
            else:
                fade_surf.fill((0, 0, 0, 255 * (fade_timer / 60)))
            screen.blit(fade_surf, (0, 0))
            fade_timer -= 1
            if fade_timer == 60:
                state = new_state

        frame = pygame.transform.scale(screen, (WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR))
        final_scaled.fill("black")
        final_scaled.blit(frame, OFFSET)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
