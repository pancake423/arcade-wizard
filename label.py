import pygame


class Label:
    def __init__(self, x, y, text, fontsize=50, centered=False):
        self.x = x
        self.y = y
        self.centered = centered
        self.font = pygame.font.Font('basis33.ttf', fontsize)
        self.surf = self.font.render(text, False, "black")
        self.rect = pygame.Rect(0, 0, *self.surf.get_size())
        self.rect.centery = y
        self.rect.left = x
        if self.centered:
            self.rect.centerx = x

    def relabel(self, new_text):
        self.surf = self.font.render(new_text, False, "black")
        self.rect = pygame.Rect(0, 0, *self.surf.get_size())
        self.rect.centery = self.y
        self.rect.left = self.x
        if self.centered:
            self.rect.centerx = self.x

    def draw(self, target):
        target.blit(self.surf, self.rect)
