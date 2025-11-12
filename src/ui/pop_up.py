import pygame
from typing import List, Tuple, Optional
from src.ui.pop_up_layout_utils import center_popup
from src.ui.pop_up_render_utils import draw_popup_background, draw_overlay
from src.ui.button_manager import ButtonManager


class Popup:
    """Flexible popup container that lays out title, optional images, body lines, and buttons.

    Usage:
        popup = Popup(title, body_lines=[...], images=[surf1, surf2], buttons=[(label, action, color)])
        popup.render(screen, button_manager)

    The popup computes its height based on content and centers itself; button_manager is used
    to register the popup buttons (it will be cleared first).
    """

    def __init__(
        self,
        title: Optional[str] = None,
        body_lines: Optional[List[str]] = None,
        images: Optional[List[pygame.Surface]] = None,
        buttons: Optional[List[Tuple[str, str, Tuple[int, int, int]]]] = None,
        width: int = 400,
        padding: int = 20,
        spacing: int = 10,
        title_font: Optional[pygame.font.Font] = None,
        body_font: Optional[pygame.font.Font] = None,
    ):
        self.title = title
        self.body_lines = body_lines or []
        self.images = images or []
        # buttons: list of (label, action, color)
        self.buttons = buttons or []
        self.width = width
        self.padding = padding
        self.spacing = spacing
        self.title_font = title_font
        self.body_font = body_font

    def _ensure_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 48)
        if self.body_font is None:
            self.body_font = pygame.font.SysFont('Arial', 18)

    def compute_height(self, screen: pygame.Surface) -> int:
        """Compute required popup height based on title, images, body lines, and buttons."""
        self._ensure_fonts()
        h = 0
        if self.title:
            title_surf = self.title_font.render(self.title, True, (0, 0, 0))
            h += title_surf.get_height()
            h += self.spacing
        # images
        for img in self.images:
            h += img.get_height()
            h += self.spacing
        # body lines
        for line in self.body_lines:
            line_surf = self.body_font.render(line, True, (0, 0, 0))
            h += line_surf.get_height()
            h += self.spacing
        # buttons area
        if self.buttons:
            btn_height = 40
            # account for all stacked buttons: each button contributes its height
            # plus the spacing that follows it (render() advances cursor by btn_h + spacing)
            h += len(self.buttons) * (btn_height + self.spacing)
        # remove last extra spacing
        if h > 0:
            h -= self.spacing
        # add vertical padding
        h += 2 * self.padding
        return h

    def render(self, screen: pygame.Surface, button_manager: ButtonManager, center=True):
        """Render the popup and register buttons into the provided ButtonManager.

        Returns the popup rect.
        """
        self._ensure_fonts()
        # Draw overlay
        draw_overlay(screen, (0, 0, 0))

        popup_h = self.compute_height(screen)
        popup_w = self.width
        if center:
            popup_x, popup_y = center_popup(screen.get_width(), screen.get_height(), popup_w, popup_h)
        else:
            # fallback to top-left
            popup_x, popup_y = (0, 0)

        # background
        draw_popup_background(screen, (255, 255, 255), popup_x, popup_y, popup_w, popup_h)

        # layout cursor
        cursor_y = popup_y + self.padding
        center_x = popup_x + popup_w // 2

        # title
        if self.title:
            title_surf = self.title_font.render(self.title, True, (0, 0, 0))
            title_rect = title_surf.get_rect(centerx=center_x, top=cursor_y)
            screen.blit(title_surf, title_rect)
            cursor_y = title_rect.bottom + self.spacing

        # images
        for img in self.images:
            img_rect = img.get_rect(centerx=center_x, top=cursor_y)
            screen.blit(img, img_rect)
            cursor_y = img_rect.bottom + self.spacing

        # body lines
        for line in self.body_lines:
            line_surf = self.body_font.render(line, True, (0, 0, 0))
            line_rect = line_surf.get_rect(centerx=center_x, top=cursor_y)
            screen.blit(line_surf, line_rect)
            cursor_y = line_rect.bottom + self.spacing

        # buttons
        # Clear previous buttons and add new ones centered horizontally stacked vertically
        button_manager.clear()
        if self.buttons:
            btn_w = min((popup_w - 2 * self.padding), 240)
            btn_h = 40
            btn_x = popup_x + (popup_w - btn_w) // 2
            # place buttons with spacing
            for label, action, color in self.buttons:
                button_manager.add_button(rect=(btn_x, cursor_y, btn_w, btn_h), label=label, action=action, color=color, text_color=(255,255,255))
                cursor_y += btn_h + self.spacing

        # Draw buttons immediately so popup owns its visuals and cursor state
        buttons_font = pygame.font.SysFont('Arial', 18, bold=True)
        button_manager.draw(screen, buttons_font)
        button_manager.set_cursor()

        return pygame.Rect(popup_x, popup_y, popup_w, popup_h)
