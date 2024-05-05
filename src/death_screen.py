from src.button import Button
from src.label import Label
from src.background import Background
from src.shop import Shop
from src.sprite import Sprite
from src.config import Images

target = None
title = None
score = None
button = None
skull = None
high_score_label = None
bg = Background()


def init(c, t, raw_score):
    global title
    global button
    global target
    global score
    global high_score_label
    global skull
    new_high_score = False
    high_score = read_highscore()
    if raw_score > high_score:
        new_high_score = True
        high_score = raw_score
        write_highscore(high_score)
    title = Label(600, 400, "You Died", 100, True, background_color=(205, 42, 21, 160))
    score = Label(10, 75, f"You survived for: {Shop.time_as_string()}", 50, False, background_color=(0, 0, 0, 64))
    high_score_label = Label(
        10, 175, "New High Score!" if new_high_score else f"High score: {Shop.time_as_string(high_score)}",
        50, False, background_color=(0, 0, 0, 64))
    button = Button(600, 700, 400, 75, "Play Again?", callback=c, textcolor="white")
    target = t
    skull = Sprite(Images.dead_wizard, 600, 525)


def step():
    bg.draw(target)
    button.update()
    skull.draw(target)
    title.draw(target)
    score.draw(target)
    high_score_label.draw(target)
    button.draw(target)


def read_highscore():
    high_score = 0
    try:
        with open('src/highscore.txt', "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        pass  # highscore will just stay zero if no file exists
    return high_score


def write_highscore(score):
    with open('src/highscore.txt', 'w') as f:
        f.write(str(score))
