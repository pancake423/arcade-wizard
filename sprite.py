import pygame


class Sprite:
    def __init__(self, image_or_surface, x=0, y=0):
        if type(image_or_surface) is pygame.Surface:
            # user passed the surface to use directly
            self.surf = image_or_surface
        else:
            # user passed a filename to an image
            self.surf = pygame.image.load(image_or_surface)

        self.x = x
        self.y = y
        self.w, self.h = self.surf.get_size()

    def draw(self, target, offset_x=0, offset_y=0):
        target.blit(self.surf, (self.x - offset_x - self.w//2, self.y - offset_y - self.h//2))
