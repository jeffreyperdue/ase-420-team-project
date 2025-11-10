import pygame
class Button:
    def __init__(self, rect, label, action, color, text_color, hover_color=None, click_color=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else self._brighten(color)
        self.click_color = click_color if click_color else self._darken(color)
        self.clicked = False

    def _darken(self, color, factor=0.8):
        return tuple(max(int(c * factor), 0) for c in color)

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.clicked:
            current_color = self.click_color
        elif self.is_hovered(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        text_surface = font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def _brighten(self, color, factor=1.2):
        return tuple(min(int(c * factor), 255) for c in color)