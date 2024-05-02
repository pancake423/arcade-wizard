from button import Button
from label import Label
from background import Background
from shop import Shop

target = None
title = None
score = None
button = None
bg = Background()


def init(c, t):
    global title
    global button
    global target
    global score
    title = Label(600, 250, "You Died!", 75, True)
    score = Label(600, 350, f"You lived for {Shop.time_as_string()}", 75, True)
    button = Button(600, 700, 400, 75, "Play Again?", callback=c)
    target = t

def step():
    bg.draw(target)
    button.update()
    title.draw(target)
    score.draw(target)
    button.draw(target)
