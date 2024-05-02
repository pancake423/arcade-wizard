import pygame
from src.button import Button
from src.label import Label
from src.weapon import Weapon
from math import ceil


class Shop:
    easter_egg = True
    gold = 200
    time_alive = None
    margin = None
    font = None
    coin = None
    coin_rect = None
    clock = None
    clock_rect = None
    target = None
    shop_button = None
    shop_close_button = None
    is_open = False
    shop_bg = None
    buy_pierce = None
    buy_damage = None
    buy_speed = None
    buy_fire = None
    buy_ice = None
    buy_electric = None
    pierce_label = None
    damage_label = None
    speed_label = None
    fire_label = None
    ice_label = None
    electric_label = None
    weapon_label = None
    elemental_label = None
    inner_rect = None
    text = None
    discount = 0

    fire_cost = 0
    ice_cost = 0
    electric_cost = 0
    pierce_cost = 0
    damage_cost = 0
    speed_cost = 0
    cost_mult = 1.5


    @staticmethod
    def init(target):
        Shop.gold = 200
        Shop.time_alive = 0
        Shop.easter_egg = True
        Shop.discount = 0
        Shop.text = None

        Shop.margin = 25
        Shop.font = pygame.font.Font("src/basis33.ttf", 75)
        Shop.coin = pygame.image.load("src/coin.png")
        Shop.coin = pygame.transform.scale_by(Shop.coin, 0.75)
        Shop.coin_rect = pygame.Rect(Shop.margin, Shop.margin, *Shop.coin.get_size())
        Shop.clock = pygame.image.load("src/clock.png")
        Shop.clock = pygame.transform.scale_by(Shop.clock, 0.75)
        Shop.clock_rect = pygame.Rect(800, 25, *Shop.clock.get_size())
        Shop.target = target
        Shop.shop_button = Button(600, 63, 150, 75, "Shop", (0, 0, 0, 64), (50, 50, 50, 128), Shop.toggle)
        Shop.shop_close_button = Button(1150, 150, 45, 45, "x", (249, 53, 90), (251, 114, 138), Shop.toggle)
        Shop.shop_bg = pygame.Surface((1100, 550), pygame.SRCALPHA)
        Shop.shop_bg.fill((100, 100, 100))
        Shop.inner_rect = pygame.Surface((500, 450), pygame.SRCALPHA)
        Shop.inner_rect.fill((80, 80, 80))

        Shop.buy_pierce = Button(500, 350, 100, 75, "Buy", (54, 141, 249), (115, 175, 251), Shop.pierce, textcolor="white")
        Shop.buy_damage = Button(500, 450, 100, 75, "Buy", (54, 141, 249), (115, 175, 251), Shop.damage, textcolor="white")
        Shop.buy_speed = Button(500, 550, 100, 75, "Buy", (54, 141, 249), (115, 175, 251), Shop.speed, textcolor="white")
        Shop.buy_fire = Button(1050, 350, 100, 75, "Buy", (54, 141, 249), (115, 175, 251), Shop.fire, textcolor="white")
        Shop.buy_ice = Button(1050, 450, 100, 75, "Buy", (54, 141, 249), (115, 175, 251), Shop.ice, textcolor="white")
        Shop.buy_electric = Button(1050, 550, 100, 75, "Buy", (54, 141, 249), (115, 175, 251), Shop.electric, textcolor="white")
        Shop.pierce_label = Label(100, 350, "Pierce ($200)", fontsize=40, textcolor="white")
        Shop.damage_label = Label(100, 450, "Damage ($200)", fontsize=40, textcolor="white")
        Shop.speed_label = Label(100, 550, "Speed ($200)", fontsize=40, textcolor="white")
        Shop.fire_label = Label(650, 350, "Fire ($200)", fontsize=40, textcolor="white")
        Shop.ice_label = Label(650, 450, "Ice ($200)", fontsize=40, textcolor="white")
        Shop.electric_label = Label(650, 550, "Electric ($200)", fontsize=40, textcolor="white")
        Shop.weapon_label = Label(325, 250, "Weapon Upgrades", centered=True, textcolor="white")
        Shop.elemental_label = Label(875, 250, "Elemental Upgrades", centered=True, textcolor="white")
        Shop.fire_cost = 200
        Shop.ice_cost = 200
        Shop.electric_cost = 200
        Shop.pierce_cost = 200
        Shop.damage_cost = 200
        Shop.speed_cost = 200
        Shop.cost_mult = 1.5

    @staticmethod
    def add_gold(amt):
        Shop.gold += amt

    @staticmethod
    def toggle():
        if Shop.is_open:
            Shop.is_open = False
        else:
            Shop.is_open = True
            Shop.pierce_label.relabel(f"Pierce (${Shop.pierce_cost})")
            Shop.damage_label.relabel(f"Damage (${Shop.damage_cost})")
            Shop.speed_label.relabel(f"Speed (${Shop.speed_cost})")

    @staticmethod
    def tick():
        Shop.time_alive += 1
        Shop.shop_button.update()

    @staticmethod
    def time_as_string(t=None):
        seconds = Shop.time_alive // 60 if t is None else t // 60
        minutes = seconds // 60
        hours = minutes // 60
        seconds %= 60
        minutes %= 60

        return f'{str(hours)}:{str(minutes).rjust(2, "0")}:{str(seconds).rjust(2, "0")}'

    @staticmethod
    def draw_ui():
        #  draw gold counter, time alive counter
        Shop.target.blit(Shop.coin, Shop.coin_rect)
        coin_text = Shop.font.render(str(Shop.gold), False, "Black")
        Shop.target.blit(coin_text, (
            Shop.coin_rect.right + Shop.margin,
            Shop.coin_rect.centery - 32
        ))
        if Shop.text is not None:
            Shop.text.draw(Shop.target)

        shop_text = Shop.font.render(Shop.time_as_string(), False, "Black")
        start = 1200 - shop_text.get_width() - Shop.clock_rect.width - Shop.margin*2
        Shop.clock_rect.left = start
        Shop.target.blit(Shop.clock, Shop.clock_rect)
        Shop.target.blit(shop_text, (
            Shop.clock_rect.right + Shop.margin,
            Shop.clock_rect.centery - 32
        ))
        Shop.shop_button.draw(Shop.target)

    @staticmethod
    def draw_shop(target):
        target.blit(Shop.shop_bg, (50, 150))
        Shop.shop_close_button.draw(target)
        target.blit(Shop.inner_rect, (75, 200))
        target.blit(Shop.inner_rect, (625, 200))
        Shop.buy_pierce.draw(target)
        Shop.buy_damage.draw(target)
        Shop.buy_speed.draw(target)
        Shop.buy_fire.draw(target)
        Shop.buy_ice.draw(target)
        Shop.buy_electric.draw(target)
        Shop.pierce_label.draw(target)
        Shop.damage_label.draw(target)
        Shop.speed_label.draw(target)
        Shop.fire_label.draw(target)
        Shop.ice_label.draw(target)
        Shop.electric_label.draw(target)
        Shop.weapon_label.draw(target)
        Shop.elemental_label.draw(target)

    @staticmethod
    def scale_cost(cost):
        Shop.easter_egg = False
        return ceil(Shop.cost_mult * cost / 50) * 50

    @staticmethod
    def update_shop():
        Shop.shop_close_button.update()
        Shop.shop_button.update()
        Shop.buy_pierce.update()
        Shop.buy_damage.update()
        Shop.buy_speed.update()
        Shop.buy_fire.update()
        Shop.buy_ice.update()
        Shop.buy_electric.update()

    @staticmethod
    def pierce():
        if Shop.gold >= Shop.pierce_cost:
            Shop.gold -= Shop.pierce_cost
            Shop.pierce_cost = Shop.scale_cost(Shop.pierce_cost)
            Shop.pierce_label.relabel(f"Pierce (${Shop.pierce_cost})")
            Weapon.pierce += 1

    @staticmethod
    def damage():
        if Shop.gold >= Shop.damage_cost:
            Shop.gold -= Shop.damage_cost
            Shop.damage_cost = Shop.scale_cost(Shop.damage_cost)
            Shop.damage_label.relabel(f"Damage (${Shop.damage_cost})")
            Weapon.damage += 2

    @staticmethod
    def speed():
        if Shop.gold >= Shop.speed_cost:
            Shop.gold -= Shop.speed_cost
            Shop.speed_cost = Shop.scale_cost(Shop.speed_cost)
            Shop.speed_label.relabel(f"Speed (${Shop.speed_cost})")
            Weapon.fire_rate = round(Weapon.fire_rate * 0.92)

    @staticmethod
    def fire():
        if Shop.gold >= Shop.fire_cost:
            Shop.gold -= Shop.fire_cost
            Shop.fire_cost = Shop.scale_cost(Shop.fire_cost)
            Shop.fire_label.relabel(f"Fire (${Shop.fire_cost})")
            Weapon.proj_type = 'src/bolt-fire.png'
            Weapon.particle_type = 'src/particle-fire.png'
            Weapon.burn_damage += 0.75
            Weapon.burn_duration = 120
            Shop.buy_electric.lock()
            Shop.buy_ice.lock()

    @staticmethod
    def ice():
        if Shop.gold >= Shop.ice_cost:
            Shop.gold -= Shop.ice_cost
            Shop.ice_cost = Shop.scale_cost(Shop.ice_cost)
            Shop.ice_label.relabel(f"Ice (${Shop.ice_cost})")
            Weapon.proj_type = 'src/bolt-ice.png'
            Weapon.particle_type = 'src/particle-ice.png'
            Weapon.slow_amount = 0.5
            Weapon.slow_duration += 10
            Shop.buy_fire.lock()
            Shop.buy_electric.lock()

    @staticmethod
    def electric():
        if Shop.gold >= Shop.electric_cost:
            Shop.gold -= Shop.electric_cost
            Shop.electric_cost = Shop.scale_cost(Shop.electric_cost)
            Shop.electric_label.relabel(f"Electric (${Shop.electric_cost})")
            Weapon.proj_type = 'src/bolt-electric.png'
            Weapon.particle_type = 'src/particle-electric.png'
            Weapon.shock_damage += 2
            Weapon.shock_radius = 100
            Shop.buy_fire.lock()
            Shop.buy_ice.lock()

    @staticmethod
    def ee_text():
        Shop.discount += 1
        if Shop.discount == 1:
            Shop.text = Label(
                25, 750, "Your persistence is admirable. 25% off.",
                background_color=(0, 0, 0, 128), fontsize=25
            )
        elif Shop.discount == 2:
            Shop.text.relabel("Still alive, huh. How about 50% off?")
        elif Shop.discount == 3:
            Shop.text.relabel("Most impressive! 75% off for you!")
