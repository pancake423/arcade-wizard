import pygame
from button import Button
from label import Label
from background import Background
from particle import ParticleManager
from random import randint
from math import sin

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
    title_1 = Label(550, 100, "Wizard", 100, True, background_color=(255, 255, 255, 128))
    title_2 = Label(650, 220, "Arcade", 100, True, background_color=(255, 255, 255, 128))
    button = Button(600, 700, 250, 75, "Start", callback=c)
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
    particles.spawn('wizard.png', -100 if d == 1 else 1300, height, mx=d*9, lifespan=200)
    particles.spawn('zombie-normal.png', -300 if d == 1 else 1500, height+15, mx=d*8, lifespan=200)

