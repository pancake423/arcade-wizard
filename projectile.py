from sprite import Sprite
from weapon import Weapon
from math import sin, cos


class Projectile(Sprite):
    def __init__(self, x, y, direction):
        super().__init__(Weapon.proj_type, x, y)
        self.direction = direction
        self.speed = Weapon.speed
        self.pierce_remaining = Weapon.pierce
        self.damage = Weapon.damage
        self.has_hit = []
        self.life_remaining = Weapon.lifespan
        self.dead = False

    def update(self, zombies):
        self.x += cos(self.direction) * self.speed
        self.y += sin(self.direction) * self.speed
        self.life_remaining -= 1

        for z in zombies.zombies:
            if z.collide_point((self.x, self.y)) and z.id not in self.has_hit:
                self.has_hit.append(z.id)
                self.pierce_remaining -= 1
                z.health -= Weapon.damage


class ProjectileManager:
    def __init__(self):
        self.projectiles = []

    def spawn_projectile(self, x, y, direction):
        self.projectiles.append(Projectile(x, y, direction))

    def update(self, zombies):
        need_kill = False
        for p in self.projectiles:
            p.update(zombies)
            if p.life_remaining <= 0 or p.pierce_remaining <= 0:
                p.dead = True
                need_kill = True
        if need_kill:
            self.projectiles[:] = [p for p in self.projectiles if not p.dead]

    def draw(self, target, offset_x, offset_y):
        for p in self.projectiles:
            p.draw(target, offset_x, offset_y, angle=p.direction)
