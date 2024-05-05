import pygame
from src.config import Fonts


class Label:
    def __init__(self, x, y, text, fontsize=50, centered=False, background_color=(0, 0, 0, 0), padding=10, textcolor="black"):
        self.x = x
        self.y = y
        self.centered = centered
        self.font = pygame.font.Font(Fonts.basis, fontsize)
        self.surf = self.font.render(text, False, textcolor)
        self.rect = pygame.Rect(0, 0, *self.surf.get_size())
        self.rect.centery = y
        self.rect.left = x
        self.bg = None
        self.textcolor = textcolor
        if self.centered:
            self.rect.centerx = x
        self.padding = padding
        if background_color[3] != 0:
            self.bg = pygame.Surface((self.rect.w + padding*2, self.rect.h + padding*2), pygame.SRCALPHA)
            self.bg.fill(background_color)


    def relabel(self, new_text):
        self.surf = self.font.render(new_text, False, self.textcolor)
        self.rect = pygame.Rect(0, 0, *self.surf.get_size())
        self.rect.centery = self.y
        self.rect.left = self.x
        if self.centered:
            self.rect.centerx = self.x

    def draw(self, target):
        if self.bg is not None:
            target.blit(self.bg, (self.rect.x - self.padding, self.rect.y - self.padding))
        target.blit(self.surf, self.rect)
