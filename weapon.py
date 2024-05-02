class Weapon:
    proj_type = 'bolt-standard.png'
    particle_type = 'particle-standard.png'
    damage = 10
    pierce = 1
    lifespan = 120
    fire_rate = 60
    speed = 15

    @staticmethod
    def reset():
        Weapon.proj_type = 'bolt-standard.png'
        Weapon.particle_type = 'particle-standard.png'
        Weapon.damage = 10
        Weapon.pierce = 1
        Weapon.lifespan = 120
        Weapon.fire_rate = 60
        Weapon.speed = 15
