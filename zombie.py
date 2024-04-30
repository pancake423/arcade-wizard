from sprite import Sprite
from math import atan2, dist, sin, cos


class ZombieStats:
    def __init__(self, image, speed, health, damage, cooldown):
        self.image = image  # image source for zombie
        self.speed = speed  # speed in pixels/frame
        self.health = health  # health
        self.damage = damage  # damage per attack
        self.atk_cooldown = cooldown  # number of frames between attacks


class Zombie(Sprite):
    baby_stats = ZombieStats('zombie-baby.png', 7, 50, 5, 30)
    normal_stats = ZombieStats('zombie-normal.png', 5, 100, 5, 60)
    giant_stats = ZombieStats('zombie-giant.png', 3, 500, 20, 120)

    @staticmethod
    def get_stats(t):
        if t == "baby":
            return Zombie.baby_stats
        if t == "normal":
            return Zombie.normal_stats
        if t == "giant":
            return Zombie.giant_stats

    def __init__(self, x, y, t):
        self.stats = Zombie.get_stats(t)
        self.cooldown = self.stats.atk_cooldown
        self.health = self.stats.health
        self.dead = False
        super().__init__(self.stats.image, x, y)

    def update(self, player):
        # walk towards player, attack if close enough
        angle = atan2(player.y_pos - self.y, player.x_pos - self.x)
        distance = dist((player.x_pos, player.y_pos), (self.x, self.y))
        move_dist = min(distance, self.stats.speed)

        self.x += cos(angle) * move_dist
        self.y += sin(angle) * move_dist

        if self.cooldown > 0:
            self.cooldown -= 1
        if distance < self.w and self.cooldown == 0:
            # apply attack
            self.cooldown = self.stats.atk_cooldown


class ZombieManager:
    def __init__(self):
        self.zombies = []

    def spawn(self, x, y, t):
        self.zombies.append(Zombie(x, y, t))

    def update(self, player):
        need_kill = False
        for z in self.zombies:
            z.update(player)
            if z.health < 0:
                # de-spawn, give gold equal to z.stats.health
                z.dead = True
                need_kill = True
        if need_kill:
            self.zombies[:] = [z for z in self.zombies if not z.dead]

    def draw(self, target, offset_x=0, offset_y=0):
        for z in self.zombies:
            z.draw(target, offset_x, offset_y)
