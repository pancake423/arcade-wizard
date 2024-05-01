from sprite import Sprite
from particle import ParticleManager
from weapon import Weapon
from math import sin, cos


class Projectile(Sprite):
    particle_freq = 5
    def __init__(self, x, y, direction, particles):
        super().__init__(Weapon.proj_type, x, y)
        self.particles = particles
        self.direction = direction
        self.speed = Weapon.speed
        self.pierce_remaining = Weapon.pierce
        self.damage = Weapon.damage
        self.has_hit = []
        self.life_remaining = Weapon.lifespan
        self.dead = False
        self.particle_timer = 0

    def update(self, zombies):
        self.x += cos(self.direction) * self.speed
        self.y += sin(self.direction) * self.speed
        self.life_remaining -= 1

        self.particle_timer += 1
        if self.particle_timer >= Projectile.particle_freq:
            self.particle_timer = 0
            self.particles.spawn(Weapon.particle_type, self.x, self.y, mr=0.1, fadeout=True, lifespan=30)

        for z in zombies.zombies:
            if z.collide_point((self.x, self.y)) and z.id not in self.has_hit:
                self.has_hit.append(z.id)
                self.pierce_remaining -= 1
                z.health -= Weapon.damage


class ProjectileManager:
    def __init__(self, bounds):
        self.projectiles = []
        self.particles = ParticleManager()
        self.bounds = bounds

    def spawn_projectile(self, x, y, direction):
        self.projectiles.append(Projectile(x, y, direction, self.particles))

    def bounds_check(self, proj):
        return (proj.x < self.bounds[0] // -2
                or proj.x > self.bounds[0] // 2
                or proj.y < self.bounds[1] // -2
                or proj.y > self.bounds[1] // 2)

    def update(self, zombies):
        self.particles.update()
        need_kill = False
        for p in self.projectiles:
            p.update(zombies)
            if p.life_remaining <= 0 or p.pierce_remaining <= 0 or self.bounds_check(p):
                p.dead = True
                need_kill = True
        if need_kill:
            self.projectiles[:] = [p for p in self.projectiles if not p.dead]

    def draw(self, target, offset_x, offset_y):
        self.particles.draw(target, offset_x, offset_y)
        for p in self.projectiles:
            p.draw(target, offset_x, offset_y, angle=p.direction)
