import pygame


class Shop:
    gold = None
    time_alive = None
    margin = None
    font = None
    coin = None
    coin_rect = None
    clock = None
    clock_rect = None
    target = None

    @staticmethod
    def init(target):
        Shop.gold = 0
        Shop.time_alive = 0

        Shop.margin = 25
        Shop.font = pygame.font.Font("basis33.ttf", 75)
        Shop.coin = pygame.image.load("coin.png")
        Shop.coin = pygame.transform.scale_by(Shop.coin, 0.75)
        Shop.coin_rect = pygame.Rect(Shop.margin, Shop.margin, *Shop.coin.get_size())
        Shop.clock = pygame.image.load("clock.png")
        Shop.clock = pygame.transform.scale_by(Shop.clock, 0.75)
        Shop.clock_rect = pygame.Rect(800, 25, *Shop.clock.get_size())
        Shop.target = target

    @staticmethod
    def add_gold(amt):
        Shop.gold += amt

    @staticmethod
    def tick():
        Shop.time_alive += 1

    @staticmethod
    def time_as_string():
        seconds = Shop.time_alive // 60
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

        shop_text = Shop.font.render(Shop.time_as_string(), False, "Black")
        start = 1200 - shop_text.get_width() - Shop.clock_rect.width - Shop.margin*2
        Shop.clock_rect.left = start
        Shop.target.blit(Shop.clock, Shop.clock_rect)
        Shop.target.blit(shop_text, (
            Shop.clock_rect.right + Shop.margin,
            Shop.clock_rect.centery - 32
        ))
