from sprite import Sprite
from random import randint, choice


class Background:
    color = (72, 205, 37)
    width = 5000  # px
    height = 5000  # px
    n_objects = 100
    opts = ["grass.png", "flower_red.png", "flower_yellow.png"]

    def __init__(self):
        self.scenery = []
        for _ in range(Background.n_objects):
            sprite = Sprite(
                choice(Background.opts),
                randint(0, Background.width) - Background.width // 2,
                randint(0, Background.height) - Background.height // 2
            )

            can_spawn = True
            for obj in self.scenery:
                if obj.collide_sprite(sprite):
                    can_spawn = False
                    break
            if can_spawn:
                self.scenery.append(sprite)

    def draw(self, target, offset_x=0, offset_y=0):
        target.fill(Background.color)
        for obj in self.scenery:
            obj.draw(target, offset_x, offset_y)
