from src.sprite import Sprite
from src.particle import ParticleManager
from random import uniform, randint
from src.config import Images


class Gravestone(Sprite):
    spawn_freq = 1080
    spawn_rng = 120
    chance_normal = 0.6
    chance_baby = 0.3
    chance_giant = 0.1
    particle_frames = 60  # number of frames before spawning a zombie where particles appear
    particle_freq = 5  # particles only appear every [particle_freq] frames.

    def __init__(self, zombies, x, y, particles):
        self.timer = 300  # 5 seconds before zombies start spawning
        self.zombies = zombies
        self.particles = particles
        super().__init__(Images.gravestone, x, y)

    def update(self):
        if self.timer == 0:
            self.timer = Gravestone.spawn_freq + randint(-Gravestone.spawn_rng, Gravestone.spawn_rng)
            self.spawn()
        if self.timer > 0:
            self.timer -= 1
        if self.timer < Gravestone.particle_frames and self.timer % Gravestone.particle_freq == 0:
            self.particles.spawn(
                Images.dirt_particle, self.x + randint(-self.w//2, self.w//2), self.y + randint(0, self.h//2),
                mx=randint(-2, 2), my=-10, gravity=True, lifespan=30
            )

    def spawn(self):
        r = uniform(0, 1)
        t = 'normal'
        if Gravestone.chance_normal < r < Gravestone.chance_baby + Gravestone.chance_normal:
            t = 'baby'
        elif r > Gravestone.chance_baby + Gravestone.chance_normal:
            t = 'giant'
        self.zombies.spawn(self.x, self.y, t)


class GravestoneManager:
    spawnable_area = (5500, 5500)
    init_graves = 4
    grave_freq = 2400

    def __init__(self, zombies):
        self.gravestones = []
        self.zombies = zombies
        self.particles = ParticleManager()
        self.grave_cooldown = GravestoneManager.grave_freq
        for _ in range(GravestoneManager.init_graves):
            self.spawn()

    def random_gravestone(self):
        return Gravestone(self.zombies,
                          randint(0, GravestoneManager.spawnable_area[0]) - GravestoneManager.spawnable_area[0] // 2,
                          randint(0, GravestoneManager.spawnable_area[1]) - GravestoneManager.spawnable_area[1] // 2,
                          self.particles
                          )

    def spawn(self):
        gravestone = self.random_gravestone()
        for _ in range(10):
            ok = True
            for g in self.gravestones:
                if g.collide_sprite(gravestone):
                    ok = False
                    break
            if ok:
                break
        self.gravestones.append(gravestone)

    def draw(self, target, offset_x, offset_y):
        for g in self.gravestones:
            g.draw(target, offset_x, offset_y)
        self.particles.draw(target, offset_x, offset_y)

    def update(self):
        self.particles.update()
        for g in self.gravestones:
            g.update()
        if self.grave_cooldown > 0:
            self.grave_cooldown -= 1
        else:
            self.grave_cooldown = GravestoneManager.grave_freq
            self.spawn()
            self.zombies.upgrade_zombies()

    def reset(self):
        self.gravestones = []
        self.grave_cooldown = GravestoneManager.grave_freq
        for _ in range(GravestoneManager.init_graves):
            self.spawn()
