import pygame
from button import Button
from label import Label
from background import Background

target = None
title_1 = None
title_2 = None
button = None
bg = Background()


def init(c, t):
    global title_1
    global title_2
    global button
    global target
    title_1 = Label(600, 100, "Wizard", 100, True)
    title_2 = Label(600, 200, "Arcade", 100, True)
    button = Button(600, 700, 250, 75, "Start", callback=c)
    target = t


def step():
    bg.draw(target)
    button.update()
    title_1.draw(target)
    title_2.draw(target)
    button.draw(target)

