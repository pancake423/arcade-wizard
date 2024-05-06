from src.sprite import Sprite
from src.particle import ParticleManager
from random import uniform, randint
from src.config import Images, GravestoneSettings
from src.zombie import Zombie


class Gravestone(Sprite):

    def __init__(self, zombies, x, y, particles):
        self.timer = 300  # 5 seconds before zombies start spawning
        self.zombies = zombies
        self.particles = particles
        super().__init__(Images.gravestone, x, y)

    def update(self):
        if self.timer == 0:
            self.timer = GravestoneSettings.spawn_freq + randint(-GravestoneSettings.spawn_rng, GravestoneSettings.spawn_rng)
            self.spawn()
        if self.timer > 0:
            self.timer -= 1
        if self.timer < GravestoneSettings.particle_frames and self.timer % GravestoneSettings.particle_freq == 0:
            self.particles.spawn(
                Images.dirt_particle, self.x + randint(-self.w//2, self.w//2), self.y + randint(0, self.h//2),
                mx=randint(-2, 2), my=-10, gravity=True, lifespan=30
            )

    def spawn(self):
        r = uniform(0, 1)
        t = 'normal'
        if GravestoneSettings.chance_normal < r < GravestoneSettings.chance_baby + GravestoneSettings.chance_normal:
            t = 'baby'
        elif r > GravestoneSettings.chance_baby + GravestoneSettings.chance_normal:
            t = 'giant'

        if len(self.zombies.zombies) > GravestoneSettings.max_n_zombies:
            # find the first zombie of type t, delete it and absorb its stats
            add_health = 0
            add_speed = 1
            stats = Zombie.get_stats(t)
            for i, z in reversed(list(enumerate(self.zombies.zombies))):
                if z.stats.image == stats.image:
                    add_health = z.max_health
                    add_speed = z.max_speed / 10
                    self.zombies.zombies.pop(i)
                    break
            self.zombies.spawn(self.x, self.y, t)
            self.zombies.zombies[-1].upgrade_to_super(add_health, add_speed)
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
