import pygame

def draw_overlay(screen, color, alpha=128):
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(alpha)
    overlay.fill(color)
    screen.blit(overlay, (0, 0))

def draw_popup_background(screen, color, popup_x, popup_y, popup_width, popup_height):
    shadow_offset = 6
    shadow_color = (0, 0, 0, 60)
    shadow_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=20)
    screen.blit(shadow_surface, (popup_x + shadow_offset, popup_y + shadow_offset))
    pygame.draw.rect(screen, color, (popup_x, popup_y, popup_width, popup_height), border_radius=20)

def draw_wrapped_label(screen, font, center_x, top_y, word1, word2, color):
    label1 = font.render(word1, True, color)
    label2 = font.render(word2, True, color)
    total_height = label1.get_height() + label2.get_height()
    top = top_y - total_height // 2
    rect1 = label1.get_rect(centerx=center_x, top=top)
    rect2 = label2.get_rect(centerx=center_x, top=top + label1.get_height())
    screen.blit(label1, rect1)
    screen.blit(label2, rect2)
    return rect2.bottom

