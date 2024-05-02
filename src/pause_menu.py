from src.label import Label
import pygame

paused_labels = None
paused_background = None
target = None


def init(t):
    global paused_labels
    global paused_background
    global target
    paused_labels = [
        Label(0, 350, "Paused", background_color=(0, 0, 0, 255), fontsize=100, textcolor="white"),
        Label(0, 450, "press esc to resume", background_color=(0, 0, 0, 255), fontsize=25, textcolor="white"),
    ]
    paused_background = pygame.Surface((1200, 800), pygame.SRCALPHA)
    paused_background.fill((0, 0, 0, 64))
    target = t


def draw():
    target.blit(paused_background, (0, 0))
    for label in paused_labels:
        label.draw(target)
