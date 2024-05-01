import pygame
from math import pi


class Sprite:
    def __init__(self, image_or_surface, x=0, y=0):
        if type(image_or_surface) is pygame.Surface:
            # user passed the surface to use directly
            self.surf = image_or_surface
        else:
            # user passed a filename to an image
            self.surf = pygame.image.load(image_or_surface)

        self.surf_flip_h = pygame.transform.flip(self.surf, True, False)
        self.flipped_h = False

        self.surf_flip_v = pygame.transform.flip(self.surf, False, True)
        self.surf_flip_both = pygame.transform.flip(self.surf, True, True)
        self.flipped_v = False

        self.x = x
        self.y = y
        self.w, self.h = self.surf.get_size()

    def draw(self, target, offset_x=0, offset_y=0, angle=0):
        surf = self.get_surf()
        if angle == 0:
            target.blit(surf, (self.x - offset_x - self.w // 2, self.y - offset_y - self.h // 2))
        else:
            surf = pygame.transform.rotate(surf, angle * 180/-pi)
            w, h = surf.get_size()
            target.blit(surf, (self.x - offset_x - w // 2, self.y - offset_y - h // 2))

    def get_surf(self):
        if self.flipped_v:
            if self.flipped_h:
                return self.surf_flip_both
            else:
                return self.surf_flip_v
        else:
            if self.flipped_h:
                return self.surf_flip_h
            else:
                return self.surf

    def collide_point(self, point):
        return abs(point[0] - self.x) <= self.w // 2 and abs(point[1] - self.y) <= self.h // 2

    def collide_sprite(self, sprite):
        self_x_range = (self.x - self.w//2, self.x + self.w//2)
        sprite_x_range = (sprite.x - sprite.w // 2, sprite.x + sprite.w // 2)
        self_y_range = (self.y - self.h // 2, self.y + self.h // 2)
        sprite_y_range = (sprite.y - sprite.h // 2, sprite.y + sprite.h // 2)

        x_ok = (self_x_range[0] <= sprite_x_range[0] <= self_x_range[1]
                or sprite_x_range[0] <= self_x_range[0] <= sprite_x_range[1])
        y_ok = (self_y_range[0] <= sprite_y_range[0] <= self_y_range[1]
                or sprite_y_range[0] <= self_y_range[0] <= sprite_y_range[1])

        return x_ok and y_ok

