import pygame
from sprite import Sprite
from math import sin, pi, floor


class Player(Sprite):
    speed = 10
    hop_size = 10
    hop_speed = 0.2

    def __init__(self, w, h, bound_w, bound_h):
        super().__init__('wizard.png', w//2, h//2)
        self.x_pos = 0
        self.y_pos = 0
        self.center_x = w//2
        self.center_y = h//2
        self.walk_frame = 0
        self.cycle_length = floor(pi / Player.hop_speed)
        self.flipped_h = True

        self.set_bounds(bound_w, bound_h)

    def update(self):
        keys = pygame.key.get_pressed()
        mx = 0
        my = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            mx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            mx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            my -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            my += 1
        mag = 1.414 if abs(mx) + abs(my) == 2 else 1
        mx *= Player.speed / mag
        my *= Player.speed / mag

        self.x_pos += mx
        self.y_pos += my

        if self.x_pos - self.w//2 < self.min_x:
            self.x_pos = self.min_x + self.w//2
        if self.x_pos + self.w//2 > self.max_x:
            self.x_pos = self.max_x - self.w//2
        if self.y_pos - self.h//2 < self.min_y:
            self.y_pos = self.min_y + self.h//2
        if self.y_pos + self.h//2 > self.max_y:
            self.y_pos = self.max_y - self.h//2

        if mx > 0:
            self.flipped_h = True
        if mx < 0:
            self.flipped_h = False

        if abs(mx) + abs(my) > 0:
            self.walk_frame += 1
            self.walk_animate(self.walk_frame)
        else:
            if self.walk_frame > 0:
                self.walk_frame += 1
                self.walk_animate(self.walk_frame)
            else:
                self.walk_animate(0)
        if self.walk_frame > self.cycle_length:
            self.walk_frame = 0

    def walk_animate(self, frame):
        self.y = self.center_y - abs(sin(frame * Player.hop_speed)) * Player.hop_size

    def set_bounds(self, width, height):
        self.min_x = -width // 2
        self.max_x = width // 2
        self.min_y = -height // 2
        self.max_y = height // 2
