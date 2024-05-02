import pygame


class Label:
    def __init__(self, x, y, text, fontsize=50, centered=False, background_color=(0, 0, 0, 0), padding=10):
        self.x = x
        self.y = y
        self.centered = centered
        self.font = pygame.font.Font('basis33.ttf', fontsize)
        self.surf = self.font.render(text, False, "black")
        self.rect = pygame.Rect(0, 0, *self.surf.get_size())
        self.rect.centery = y
        self.rect.left = x
        self.bg = None
        if self.centered:
            self.rect.centerx = x
        self.padding = padding
        if background_color[3] != 0:
            self.bg = pygame.Surface((self.rect.w + padding*2, self.rect.h + padding*2), pygame.SRCALPHA)
            self.bg.fill(background_color)


    def relabel(self, new_text):
        self.surf = self.font.render(new_text, False, "black")
        self.rect = pygame.Rect(0, 0, *self.surf.get_size())
        self.rect.centery = self.y
        self.rect.left = self.x
        if self.centered:
            self.rect.centerx = self.x

    def draw(self, target):
        if self.bg is not None:
            target.blit(self.bg, (self.rect.x - self.padding, self.rect.y - self.padding))
        target.blit(self.surf, self.rect)
