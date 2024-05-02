import pygame


class Button:
    def __init__(self, x, y, w, h, text, color=(54, 141, 249), color_hover=(115, 175, 251), callback=None):
        self.font = pygame.font.Font("basis33.ttf", 75)
        self.body = pygame.Surface((w, h), pygame.SRCALPHA)
        self.body.fill(color)
        self.body_hover = pygame.Surface((w, h), pygame.SRCALPHA)
        self.body_hover.fill(color_hover)
        self.text = self.font.render(text, False, "black")
        self.text_rect = pygame.Rect(0, 0, *self.text.get_size())
        self.text_rect.center = (x, y)
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.active = False
        self.primed = False
        self.callback = callback

    def draw(self, target):
        target.blit(self.body_hover if self.active else self.body, self.rect)
        target.blit(self.text, self.text_rect)

    def update(self):
        self.active = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.active:
            if pygame.mouse.get_pressed()[0]:
                self.primed = True
            elif self.primed:
                if self.callback is not None:
                    self.callback()
                self.primed = False
        else:
            self.primed = False

