import pygame
from src.sprite import Sprite
from math import sin, pi, floor, atan2
from src.config import Weapon, Images, PlayerSettings
from src.health_bar import HealthBar
from src.shop import Shop
from src.particle import ParticleManager
from random import randint, uniform


class Player:

    def __init__(self, w, h, bound_w, bound_h, proj):
        self.sprite = Sprite(Images.wizard_1, w//2, h//2)
        self.x_pos = 0
        self.y_pos = 0
        self.center_x = w//2
        self.center_y = h//2
        self.walk_frame = 0
        self.cycle_length = floor(pi / PlayerSettings.hop_speed)
        self.flipped_h = True
        self.proj = proj
        self.fire_cooldown = 0
        self.health = PlayerSettings.max_health
        self.heal_cooldown = PlayerSettings.heal_cooldown
        self.center = (w//2, h//2)
        self.particles = ParticleManager()

        self.set_bounds(bound_w, bound_h)

    def draw(self, target):
        self.sprite.draw(target)
        HealthBar.draw(target, self.sprite, 0, 0, self.health / PlayerSettings.max_health, PlayerSettings.health_bar_color)
        self.particles.draw(target, self.x_pos - self.center_x, self.y_pos - self.center_y)

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
        mx *= PlayerSettings.speed / mag
        my *= PlayerSettings.speed / mag

        self.x_pos += mx
        self.y_pos += my

        if self.x_pos - self.sprite.w//2 < self.min_x:
            self.x_pos = self.min_x + self.sprite.w//2
        if self.x_pos + self.sprite.w//2 > self.max_x:
            self.x_pos = self.max_x - self.sprite.w//2
        if self.y_pos - self.sprite.h//2 < self.min_y:
            self.y_pos = self.min_y + self.sprite.h//2
        if self.y_pos + self.sprite.h//2 > self.max_y:
            self.y_pos = self.max_y - self.sprite.h//2

        if mx > 0:
            self.sprite.flipped_h = True
        if mx < 0:
            self.sprite.flipped_h = False

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

        # shoot projectiles if mouse down
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        if pygame.mouse.get_pressed()[0] and self.fire_cooldown <= 0 and not Shop.shop_button.primed:
            self.fire_cooldown = Weapon.fire_rate
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.proj.spawn_projectile(self.x_pos, self.y_pos, atan2(mouse_y - self.center_y, mouse_x - self.center_x))

        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        else:
            if self.health < self.max_health:
                self.health += PlayerSettings.regen_amt

        t = Shop.time_alive
        if t % 60 == 0:
            self.add_sparkle()
        if Shop.time_alive == 60 * 60 * 5:
            self.set_image(Images.wizard_2)
            self.survival_buff()
        if Shop.time_alive == 60 * 60 * 10:
            self.set_image(Images.wizard_3)
            self.survival_buff()
        if Shop.time_alive == 60 * 60 * 15:
            self.set_image(Images.wizard_4)
            self.survival_buff()
        self.particles.update()

    def survival_buff(self):
        if Shop.easter_egg:
            Shop.ee_text()
            Shop.buy_fire.lock()
            Shop.buy_electric.lock()
            Shop.buy_ice.lock()
            Shop.pierce_cost -= 50
            Shop.damage_cost -= 50
            Shop.speed_cost -= 50
            Shop.cost_mult -= 0.1
            Weapon.proj_type = Images.bolt_secret
            Weapon.particle_type = Images.particle_secret
        self.add_sparkle(50, 10, 90)
        Weapon.damage += 10
        Weapon.pierce += 2
        Weapon.fire_rate *= 0.8

    def add_sparkle(self, n=1, speed=0, duration=30):
        for _ in range(n):
            self.particles.spawn(
                Weapon.particle_type,
                self.x_pos + randint(-self.sprite.w // 2, self.sprite.w // 2),
                self.y_pos + randint(-self.sprite.h // 2, self.sprite.h // 2),
                lifespan=duration, fadeout=True, mr=0.1, mx=uniform(-speed, speed), my=uniform(-speed, speed)
            )

    def walk_animate(self, frame):
        self.sprite.y = self.center_y - abs(sin(frame * PlayerSettings.hop_speed)) * PlayerSettings.hop_size

    def set_bounds(self, width, height):
        self.min_x = -width // 2
        self.max_x = width // 2
        self.min_y = -height // 2
        self.max_y = height // 2

    def reset(self):
        self.x_pos = 0
        self.y_pos = 0
        self.health = PlayerSettings.max_health
        self.set_image(Images.wizard_1)
        Player.speed = 10

    def damage(self, amt):
        self.health -= amt
        self.heal_cooldown = PlayerSettings.heal_cooldown

    def set_image(self, image):
        self.sprite = Sprite(image, *self.center)

