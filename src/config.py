"""
config.py
Holds all program constants for the entire game.
This file allows you to easily modify assets and game balance.
"""


# reference to all font files used in the game.
class Fonts:
    basis = "src/assets/basis33.ttf"


# reference to all image files used in the game.
class Images:
    bite_effect = "src/assets/bite-effect.png"
    bolt_electric = "src/assets/bolt-electric.png"
    bolt_fire = "src/assets/bolt-fire.png"
    bolt_ice = "src/assets/bolt-ice.png"
    bolt_secret = "src/assets/bolt-secret.png"
    bolt_standard = "src/assets/bolt-standard.png"
    clock = "src/assets/clock.png"
    coin = "src/assets/coin.png"
    dead_wizard = "src/assets/dead-wizard.png"
    dirt_particle = "src/assets/dirt-particle.png"
    flower_red = "src/assets/flower-red.png"
    flower_yellow = "src/assets/flower-yellow.png"
    grass = "src/assets/grass.png"
    gravestone = "src/assets/gravestone.png"
    hedge = "src/assets/hedge.png"
    particle_electric = "src/assets/particle-electric.png"
    particle_fire = "src/assets/particle-fire.png"
    particle_ice = "src/assets/particle-ice.png"
    particle_secret = "src/assets/particle-secret.png"
    particle_standard = "src/assets/particle-standard.png"
    wizard_1 = "src/assets/wizard-1.png"
    wizard_2 = "src/assets/wizard-2.png"
    wizard_3 = "src/assets/wizard-3.png"
    wizard_4 = "src/assets/wizard-4.png"
    wizard_head = "src/assets/wizard-head.png"
    zombie_baby = "src/assets/zombie-baby.png"
    zombie_giant = "src/assets/zombie-giant.png"
    zombie_normal = "src/assets/zombie-normal.png"


# Player weapon statistics (base).
class Weapon:
    proj_type = Images.bolt_standard
    particle_type = Images.particle_standard
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
        Weapon.proj_type = Images.bolt_standard
        Weapon.particle_type = Images.particle_standard
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


# controls the stats and scaling of the zombies.

class ZombieStats:
    def __init__(self, image, speed, health, damage, cooldown):
        self.image = image  # image source for zombie
        self.speed = speed  # speed in pixels/frame
        self.health = health  # health
        self.damage = damage  # damage per attack
        self.atk_cooldown = cooldown  # number of frames between attacks


class ZombieSettings:
    baby_stats = ZombieStats(Images.zombie_baby, 7, 50, 5, 30)
    normal_stats = ZombieStats(Images.zombie_normal, 5, 100, 5, 60)
    giant_stats = ZombieStats(Images.zombie_giant, 3, 500, 20, 120)

    zombie_scale_factor = 1.02  # controls the rate at which zombies scale every time they upgrade.
    health_scale_multiplier = 4  # health scales by a factor of [health_scale_multiplier] more than speed.
    speed_cap = 9.5  # max speed that zombies can reach

    bite_radius = 1.5  # bite radius as a multiple of sprite size
    repel_radius = 100  # maximum repulsion radius in pixels
    repel_force = 0.6  # repulsion force as a fraction of distance
    active_distance_threshold = 2400  # zombies must be within this distance of the player to move.

    health_bar_color = (252, 88, 59)

    hop_size = 10
    hop_speed = 0.02

    n_move = 20  # number of zombies guaranteed to move every frame


class GravestoneSettings:
    spawn_freq = 1080  # number of frames between when new gravestones appear
    spawn_rng = 120  # variability in spawn time
    chance_normal = 0.6  # odds of a normal zombie spawning
    chance_baby = 0.3  # odds of a baby zombie spawning
    chance_giant = 0.1  # odds of a giant spawning
    particle_frames = 60  # number of frames before spawning a zombie where particles appear
    particle_freq = 5  # particles only appear every [particle_freq] frames.

    max_n_zombies = 75  # maximum number of zombies that can appear on screen before they start upgrading.


class PlayerSettings:
    speed = 10
    max_health = 100

    heal_cooldown = 900
    regen_amt = 0.1

    hop_size = 10
    hop_speed = 0.2

    health_bar_color = (159, 251, 118)
