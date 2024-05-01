from sprite import Sprite
from random import uniform, randint


class Gravestone(Sprite):
    spawn_freq = 1000
    chance_normal = 0.6
    chance_baby = 0.3
    chance_giant = 0.1

    def __init__(self, zombies, x, y):
        self.timer = Gravestone.spawn_freq
        self.zombies = zombies
        super().__init__('gravestone.png', x, y)

    def update(self):
        if self.timer == 0:
            self.timer = Gravestone.spawn_freq
            self.spawn()
        if self.timer > 0:
            self.timer -= 1

    def spawn(self):
        r = uniform(0, 1)
        t = 'normal'
        if Gravestone.chance_normal < r < Gravestone.chance_baby + Gravestone.chance_normal:
            t = 'baby'
        elif r > Gravestone.chance_baby + Gravestone.chance_normal:
            t = 'giant'
        self.zombies.spawn(self.x, self.y, t)


class GravestoneManager:
    spawnable_area = (4000, 4000)
    init_graves = 4
    grave_freq = 10000

    def __init__(self, zombies):
        self.gravestones = []
        self.zombies = zombies
        self.grave_cooldown = GravestoneManager.grave_freq
        for _ in range(GravestoneManager.init_graves):
            self.random_gravestone()

    def random_gravestone(self):
        return Gravestone(self.zombies,
                          randint(0, GravestoneManager.spawnable_area[0]) - GravestoneManager.spawnable_area[0] // 2,
                          randint(0, GravestoneManager.spawnable_area[1]) - GravestoneManager.spawnable_area[1] // 2,
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

    def update(self):
        for g in self.gravestones:
            g.update()
        if self.grave_cooldown > 0:
            self.grave_cooldown -= 1
        else:
            self.grave_cooldown = GravestoneManager.grave_freq
            self.random_gravestone()
