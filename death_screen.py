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
high_score = 0
high_score_label = None
bg = Background()


def init(c, t, raw_score):
    global title
    global button
    global target
    global score
    global high_score
    global high_score_label
    global skull
    new_high_score = False
    if raw_score > high_score:
        new_high_score = True
        high_score = raw_score
    title = Label(600, 400, "You Died", 100, True, background_color=(205, 42, 21, 160))
    score = Label(10, 75, f"You survived for: {Shop.time_as_string()}", 50, False, background_color=(0, 0, 0, 64))
    high_score_label = Label(
        10, 175, "New High Score!" if new_high_score else f"High score: {Shop.time_as_string(high_score)}",
        50, False, background_color=(0, 0, 0, 64))
    button = Button(600, 700, 400, 75, "Play Again?", callback=c, textcolor="white")
    target = t
    skull = Sprite("dead-wizard.png", 600, 525)

def step():
    bg.draw(target)
    button.update()
    skull.draw(target)
    title.draw(target)
    score.draw(target)
    high_score_label.draw(target)
    button.draw(target)
