import pygame
from src.button import Button
from src.label import Label
from src.background import Background
from src.particle import ParticleManager
from random import randint
from math import sin
from src.config import Images

target = None
title_1 = None
title_2 = None
button = None
bg = Background()
particles = ParticleManager()
frame = 0


def init(c, t):
    global title_1
    global title_2
    global button
    global target
    title_1 = Label(575, 100, "Wizard", 140, True, background_color=(0, 0, 0, 64))
    title_2 = Label(625, 280, "Arcade", 140, True, background_color=(0, 0, 0, 64))
    button = Button(600, 700, 250, 75, "Start", callback=c, textcolor="white")
    target = t


def step():
    global frame
    if frame % 200 == 0:
        random_wizard_animation()
    frame += 1
    bg.draw(target, offset_x=sin(frame/200) * 200)
    button.update()
    particles.update()
    particles.draw(target)
    title_1.draw(target)
    title_2.draw(target)
    button.draw(target)

def random_wizard_animation():
    d = -1 if randint(0, 1) == 1 else 1
    height = randint(100, 700)
    particles.spawn(Images.wizard_1, -100 if d == 1 else 1300, height, mx=d*9, lifespan=200)
    particles.spawn(Images.zombie_normal, -300 if d == 1 else 1500, height+15, mx=d*8, lifespan=200)

