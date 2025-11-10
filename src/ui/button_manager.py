import pygame
from src.ui.button import Button

class ButtonManager:
    def __init__(self):
        self.buttons = []

    def add_button(self, rect, label, action, color=(0, 200, 0), text_color=(255, 255, 255)):
        self.buttons.append(Button(rect, label, action, color, text_color))

    def draw(self, screen, font):
        for button in self.buttons:
            button.draw(screen, font)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_hovered(pos):
                return button.action
        return None

    def set_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        if any(button.is_hovered(mouse_pos) for button in self.buttons):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)