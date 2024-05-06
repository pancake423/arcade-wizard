from src.sprite import Sprite
from math import atan2, dist, sin, cos
from src.health_bar import HealthBar
from src.particle import ParticleManager
from src.shop import Shop
from random import randint
from src.config import Weapon, Images, ZombieSettings
from copy import copy
import pygame

baby = Sprite(Images.zombie_baby)
normal = Sprite(Images.zombie_normal)
giant = Sprite(Images.zombie_giant)


def make_stacked_image(source_image, n_stacks=1):
    print(source_image, n_stacks)
    stack_offset = 25
    out = pygame.Surface(
        (source_image.get_width() + stack_offset*n_stacks, source_image.get_height() + stack_offset*n_stacks),
        pygame.SRCALPHA
    )
    for i in range(n_stacks):
        out.blit(source_image, (i*stack_offset, i*stack_offset))
    return out


class Zombie:
    id_counter = 0

    @staticmethod
    def get_stats(t):
        if t == "baby":
            return copy(ZombieSettings.baby_stats)
        if t == "normal":
            return copy(ZombieSettings.normal_stats)
        if t == "giant":
            return copy(ZombieSettings.giant_stats)

    @staticmethod
    def get_sprite(t):
        if t == "baby":
            return baby
        if t == "normal":
            return normal
        if t == "giant":
            return giant

    def __init__(self, x, y, t, particles, scale=1):
        self.stats = Zombie.get_stats(t)
        self.cooldown = self.stats.atk_cooldown
        self.health = self.stats.health
        self.dead = False
        self.id = Zombie.id_counter
        self.angle = 0
        self.walk_frame = 0
        self.particles = particles
        self.fire_tick = 0
        self.slow_tick = 0
        self.stun_tick = 0
        Zombie.id_counter += 1
        self.y_draw = 0
        self.x = x
        self.y = y

        self.sprite = Zombie.get_sprite(t)
        self.stacks=1

        self.w = self.sprite.w
        self.h = self.sprite.h

        self.health *= scale ** ZombieSettings.health_scale_multiplier
        self.max_health = self.health
        self.stats.speed = min(self.stats.speed * scale, ZombieSettings.speed_cap)

    def upgrade_to_super(self, extra_health, extra_speed):
        self.stacks += 1
        self.max_health += extra_health
        self.health = self.max_health
        self.stats.speed = min(self.stats.speed + extra_speed, ZombieSettings.speed_cap)
        new_img = make_stacked_image(self.sprite.surf, self.stacks)
        self.sprite = Sprite(new_img, 0, 0)

    def update(self, player, zombies):
        # walk towards player
        distance = dist((player.x_pos, player.y_pos), (self.x, self.y))
        angle = atan2(player.y_pos - self.y, player.x_pos - self.x)
        move_dist = min(distance, self.stats.speed)
        if self.slow_tick > 0:
            self.slow_tick -= 1
            move_dist *= Weapon.slow_amount
            if self.slow_tick % Weapon.fire_tickrate == 0:
                self.particles.spawn(
                    Images.particle_ice,
                    self.x + randint(-self.w // 2, self.w // 2),
                    self.y + randint(-self.h // 2, self.h // 2),
                    lifespan=30, fadeout=True, mr=0.1
                )
        if self.stun_tick > 0:
            self.stun_tick -= 1
            move_dist *= 0.65

        if self.fire_tick > 0:
            self.fire_tick -= 1
            if self.fire_tick % Weapon.fire_tickrate == 0:
                self.health -= Weapon.burn_damage
                self.particles.spawn(
                    Images.particle_fire,
                    self.x + randint(-self.w // 2, self.w // 2),
                    self.y + randint(-self.h // 2, self.h // 2),
                    lifespan=30, fadeout=True, mr=0.1
                )

        self.x += cos(angle) * move_dist
        self.y += sin(angle) * move_dist

        self.walk_animate(self.walk_frame)
        self.walk_frame += 1

        # attack if in range and cooldown is up
        if self.cooldown > 0:
            self.cooldown -= 1
        if distance < self.w * ZombieSettings.bite_radius and self.cooldown == 0:
            player.damage(self.stats.damage)
            self.particles.spawn(
                Images.bite_effect,
                player.x_pos + randint(-player.sprite.w//2, player.sprite.w//2),
                player.y_pos + randint(-player.sprite.h//2, player.sprite.h//2),
                lifespan=30, fadeout=True
            )
            self.cooldown = self.stats.atk_cooldown

        # move away from other zombies in range (repulsion effect)
        for z in zombies:
            if z.id == self.id:
                continue
            distance = dist((self.x, self.y), (z.x, z.y))
            if distance < ZombieSettings.repel_radius:
                angle = atan2(self.y - z.y, self.x - z.x)
                force = (ZombieSettings.repel_radius - distance) * ZombieSettings.repel_force
                self.x += cos(angle) * force
                self.y += sin(angle) * force

    def walk_animate(self, frame):
        self.y_draw = abs(sin(frame * ZombieSettings.hop_speed * self.stats.speed)) * ZombieSettings.hop_size

    def draw(self, target, offset_x=0, offset_y=0):
        self.sprite.draw(target, offset_x - self.x, offset_y - self.y_draw - self.y)
        HealthBar.draw(
            target, self, offset_x, offset_y - self.y_draw,
            self.health / self.max_health, ZombieSettings.health_bar_color
        )

    def collide_point(self, point):
        return abs(point[0] - self.x) <= self.w // 2 and abs(point[1] - self.y) <= self.h // 2


class ZombieManager:
    def __init__(self):
        self.zombies = []
        self.particles = ParticleManager()
        self.zombie_scale = 1

    def spawn(self, x, y, t):
        self.zombies.append(Zombie(x, y, t, self.particles, self.zombie_scale))

    def update(self, player):
        self.particles.update()
        need_kill = False
        n_updated = 0
        for z in self.zombies:
            distance = dist((player.x_pos, player.y_pos), (z.x, z.y))
            if distance < ZombieSettings.active_distance_threshold or n_updated < ZombieSettings.n_move:
                n_updated += 1
                z.update(player, self.zombies)
            if z.health <= 0:
                Shop.add_gold(z.stats.health)
                z.dead = True
                need_kill = True
        if need_kill:
            self.zombies[:] = [z for z in self.zombies if not z.dead]

    def draw(self, target, offset_x=0, offset_y=0):
        for z in self.zombies:
            z.draw(target, offset_x, offset_y)
        self.particles.draw(target, offset_x, offset_y)

    def reset(self):
        self.zombies = []
        self.particles.particles = []
        self.zombie_scale = 1

    def upgrade_zombies(self):
        self.zombie_scale *= ZombieSettings.zombie_scale_factor
