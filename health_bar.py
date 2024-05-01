import pygame


class HealthBar:
    bg_color = (0, 0, 0)
    height = 10
    width = 0.75
    border_size = 2
    gap = 10

    @staticmethod
    def draw(target, sprite, offset_x, offset_y, percentage, color):
        x = sprite.x - offset_x
        y = sprite.y - offset_y
        outer_rect = pygame.Rect(
            x - (sprite.w // 2 * HealthBar.width) - HealthBar.border_size,
            y - sprite.h // 2 - HealthBar.border_size - HealthBar.gap - HealthBar.height,
            (sprite.w * HealthBar.width) + HealthBar.border_size * 2,
            HealthBar.height + HealthBar.border_size*2
        )
        inner_rect = pygame.Rect(
            x - (sprite.w // 2 * HealthBar.width), y - sprite.h // 2 - HealthBar.gap - HealthBar.height,
            (sprite.w * HealthBar.width) * percentage, HealthBar.height
        )
        pygame.draw.rect(target, HealthBar.bg_color, outer_rect, border_radius=HealthBar.gap//2)
        pygame.draw.rect(target, color, inner_rect, border_radius=HealthBar.gap // 2)
