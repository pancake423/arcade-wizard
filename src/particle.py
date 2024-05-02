from src.sprite import Sprite


class Particle(Sprite):
    gravity = 1
    max_vel = 10
    fadeout_time = 30

    def __init__(self, image, x, y, mx, my, mr, gravity, fadeout, lifespan):
        super().__init__(image, x, y)
        self.mx = mx
        self.my = my
        self.mr = mr
        self.has_gravity = gravity
        self.fades_out = fadeout
        self.time_remaining = lifespan
        self.dead = False
        self.angle = 0
        self.opacity = 255

    def update(self):
        self.x += self.mx
        self.y += self.my
        self.angle += self.mr
        self.time_remaining -= 1
        if self.has_gravity and self.my < Particle.max_vel:
            self.my += Particle.gravity
        if self.fades_out and self.time_remaining < Particle.fadeout_time:
            self.opacity = round(255 * (self.time_remaining / Particle.fadeout_time))


class ParticleManager:
    def __init__(self):
        self.particles = []

    def spawn(self, image, x, y, mx=0, my=0, mr=0, gravity=False, fadeout=False, lifespan=100):
        self.particles.append(Particle(image, x, y, mx, my, mr, gravity, fadeout, lifespan))

    def draw(self, target, offset_x=0, offset_y=0):
        for p in self.particles:
            p.draw(target, offset_x, offset_y, angle=p.angle, opacity=p.opacity)

    def update(self):
        need_kill = False
        for p in self.particles:
            p.update()
            if p.time_remaining <= 0:
                p.dead = True
                need_kill = True
        if need_kill:
            self.particles[:] = [p for p in self.particles if not p.dead]


