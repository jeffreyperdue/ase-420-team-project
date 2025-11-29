import pygame

def draw_overlay(screen, color, alpha=128):
    """Draw a semi-transparent overlay over the entire screen."""
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(alpha)
    overlay.fill(color)
    screen.blit(overlay, (0, 0))

def draw_popup_background(screen, color, popup_x, popup_y, popup_width, popup_height):
    """Draw a popup background with shadow effect."""
    shadow_offset = 6
    shadow_color = (0, 0, 0, 60)
    shadow_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=20)
    screen.blit(shadow_surface, (popup_x + shadow_offset, popup_y + shadow_offset))
    pygame.draw.rect(screen, color, (popup_x, popup_y, popup_width, popup_height), border_radius=20)
