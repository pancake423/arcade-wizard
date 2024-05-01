import pygame


class Sprite:
    def __init__(self, image_or_surface, x=0, y=0):
        if type(image_or_surface) is pygame.Surface:
            # user passed the surface to use directly
            self.surf = image_or_surface
        else:
            # user passed a filename to an image
            self.surf = pygame.image.load(image_or_surface)

        self.surf_flip_h = pygame.transform.flip(self.surf, True, False)
        self.flipped = False

        self.x = x
        self.y = y
        self.w, self.h = self.surf.get_size()

    def draw(self, target, offset_x=0, offset_y=0):
        target.blit(
            self.surf_flip_h if self.flipped else self.surf,
            (self.x - offset_x - self.w // 2, self.y - offset_y - self.h // 2)
        )

    def collide_point(self, point):
        return abs(point[0] - self.x) < self.w // 2 and abs(point[1] - self.y) < self.h // 2

    def collide_sprite(self, sprite):
        return (self.collide_point((sprite.x + sprite.w // 2, sprite.y + sprite.h // 2)) or
                self.collide_point((sprite.x - sprite.w // 2, sprite.y + sprite.h // 2)) or
                self.collide_point((sprite.x + sprite.w // 2, sprite.y - sprite.h // 2)) or
                self.collide_point((sprite.x - sprite.w // 2, sprite.y - sprite.h // 2)))
