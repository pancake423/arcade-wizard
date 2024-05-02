from button import Button
from label import Label
from background import Background
from shop import Shop
from sprite import Sprite

target = None
title = None
score = None
button = None
skull = None
bg = Background()


def init(c, t):
    global title
    global button
    global target
    global score
    global skull
    title = Label(600, 250, "You Died!", 75, True, background_color=(205, 42, 21, 160))
    score = Label(600, 350, f"You lived for {Shop.time_as_string()}", 50, True, background_color=(205, 42, 21, 160))
    button = Button(600, 700, 400, 75, "Play Again?", callback=c)
    target = t
    skull = Sprite("dead-wizard.png", 600, 500)

def step():
    bg.draw(target)
    button.update()
    skull.draw(target)
    title.draw(target)
    score.draw(target)
    button.draw(target)
