class Weapon:
    proj_type = 'src/bolt-standard.png'
    particle_type = 'src/particle-standard.png'
    damage = 10
    pierce = 2
    lifespan = 120
    fire_rate = 60
    speed = 15
    burn_duration = 0
    burn_damage = 0
    shock_radius = 0
    shock_damage = 0
    slow_duration = 0
    slow_amount = 1
    fire_tickrate = 10

    @staticmethod
    def reset():
        Weapon.proj_type = 'src/bolt-standard.png'
        Weapon.particle_type = 'src/particle-standard.png'
        Weapon.damage = 10
        Weapon.pierce = 2
        Weapon.lifespan = 120
        Weapon.fire_rate = 60
        Weapon.speed = 15
        Weapon.burn_duration = 0
        Weapon.burn_damage = 0
        Weapon.shock_radius = 0
        Weapon.shock_damage = 0
        Weapon.slow_duration = 0
        Weapon.slow_amount = 1
