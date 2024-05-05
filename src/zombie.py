from src.sprite import Sprite
from math import atan2, dist, sin, cos, sqrt
from src.health_bar import HealthBar
from src.particle import ParticleManager
from src.shop import Shop
from random import randint, uniform
from src.config import Weapon, Images, ZombieSettings
from copy import copy


class Zombie(Sprite):
    id_counter = 0

    @staticmethod
    def get_stats(t):
        if t == "baby":
            return copy(ZombieSettings.baby_stats)
        if t == "normal":
            return copy(ZombieSettings.normal_stats)
        if t == "giant":
            return copy(ZombieSettings.giant_stats)

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

        self.health *= scale ** 5
        self.max_health = self.health
        self.stats.speed = min(self.stats.speed * sqrt(scale), 9.5 if t != "baby" else 10.5)

        super().__init__(self.stats.image, x, y)

    def update(self, player, zombies):
        # walk towards player
        angle = atan2(player.y_pos - self.y, player.x_pos - self.x)
        distance = dist((player.x_pos, player.y_pos), (self.x, self.y))
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
            move_dist *= 0.7

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

        # zombie tilting animation
        self.angle = sin(self.walk_frame * self.stats.speed) * ZombieSettings.tilt_amount
        self.walk_frame += ZombieSettings.tilt_speed

        # attack if in range and cooldown is up
        if self.cooldown > 0:
            self.cooldown -= 1
        if distance < self.w * ZombieSettings.bite_radius and self.cooldown == 0:
            player.damage(self.stats.damage)
            self.particles.spawn(
                Images.bite_effect,
                player.x_pos + randint(-player.sprite.w//2, player.sprite.w//2), player.y_pos + randint(-player.sprite.h//2, player.sprite.h//2),
                lifespan=30, fadeout=True
            )
            self.cooldown = self.stats.atk_cooldown

        # move away from other zombies in range (repulsion effect)
        for z in zombies:
            if z.id == self.id:
                continue
            distance = dist((self.x, self.y), (z.x, z.y))
            if distance < 50:
                angle = atan2(self.y - z.y, self.x - z.x)
                force = (50 - distance) * ZombieSettings.repel_force
                self.x += cos(angle) * force
                self.y += sin(angle) * force


    def draw(self, target, offset_x=0, offset_y=0):
        super().draw(target, offset_x, offset_y, angle=self.angle)
        HealthBar.draw(target, self, offset_x, offset_y, self.health / self.max_health, ZombieSettings.health_bar_color)


class ZombieManager:

    def __init__(self):
        self.zombies = []
        self.particles = ParticleManager()
        self.zombie_scale = 1
        self.zombie_scale_factor = 1.02

    def spawn(self, x, y, t):
        self.zombies.append(Zombie(x, y, t, self.particles, self.zombie_scale))

    def update(self, player):
        self.particles.update()
        need_kill = False
        for z in self.zombies:
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
        self.zombie_scale *= self.zombie_scale_factor

