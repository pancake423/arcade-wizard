from src.sprite import Sprite
from random import randint, choice
from src.config import Images
import pygame


class Background:
    color = (72, 205, 37)
    outside_color = (2, 46, 6)
    width = 5000  # px
    height = 5000  # px
    n_objects = 150
    opts = [Images.grass, Images.flower_red, Images.flower_yellow]

    def __init__(self):
        self.scenery = []
        self.hedges = []
        self.player_area = pygame.Rect(-Background.width//2, -Background.height//2, Background.width, Background.height)

        for i in range(-Background.width//2, Background.width//2, 150):
            sprite1 = Sprite(Images.hedge, i, -Background.height // 2)
            sprite2 = Sprite(Images.hedge, i, Background.height // 2)
            sprite1.flipped_h = randint(0, 1) == 1
            sprite1.flipped_v = randint(0, 1) == 1
            sprite2.flipped_h = randint(0, 1) == 1
            sprite2.flipped_v = randint(0, 1) == 1
            self.hedges.append(sprite1)
            self.hedges.append(sprite2)

        for i in range(-Background.height//2, Background.height//2, 150):
            sprite1 = Sprite(Images.hedge, -Background.width // 2, i)
            sprite2 = Sprite(Images.hedge, Background.width // 2, i)
            sprite1.flipped_h = randint(0, 1) == 1
            sprite1.flipped_v = randint(0, 1) == 1
            sprite2.flipped_h = randint(0, 1) == 1
            sprite2.flipped_v = randint(0, 1) == 1
            self.hedges.append(sprite1)
            self.hedges.append(sprite2)

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
        target.fill(Background.outside_color)
        self.player_area.x = -Background.width//2 - offset_x
        self.player_area.y = -Background.height//2 - offset_y
        pygame.draw.rect(target, Background.color, self.player_area)
        for obj in self.scenery:
            obj.draw(target, offset_x, offset_y)

    def draw_hedges(self, target, offset_x=0, offset_y=0):
        for obj in self.hedges:
            obj.draw(target, offset_x, offset_y)
