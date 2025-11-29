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
        button_specs: Optional[List[Tuple[str, str, Tuple[int, int, int]]]] = None,
        popup_width: int = 400,
        padding: int = 20,
        element_spacing: int = 10,
        title_font_style: Optional[pygame.font.Font] = None,
        body_font_style: Optional[pygame.font.Font] = None,
    ):
        self.title = title
        self.body_lines = body_lines or []
        self.images = images or []
        self.button_specs = button_specs or [] # list of (label, action, color)
        self.popup_width = popup_width
        self.padding = padding
        self.element_spacing = element_spacing
        self.title_font_style = title_font_style
        self.body_font_style = body_font_style

    def _ensure_fonts(self):
        """Ensure fonts are initialized."""
        if self.title_font_style is None:
            self.title_font_style = pygame.font.Font(None, 48)
        if self.body_font_style is None:
            self.body_font_style = pygame.font.SysFont('Arial', 18)

    def compute_height(self, screen: pygame.Surface) -> int:
        """Compute required popup height based on title, images, body lines, and buttons."""
        self._ensure_fonts()
        popup_height = 0
        if self.title:
            title_surface = self.title_font_style.render(self.title, True, (0, 0, 0))
            popup_height += title_surface.get_height()
            popup_height += self.element_spacing
        # images
        for image in self.images:
            popup_height += image.get_height()
            popup_height += self.element_spacing
        # body lines
        for line in self.body_lines:
            line_surface = self.body_font_style.render(line, True, (0, 0, 0))
            popup_height += line_surface.get_height()
            popup_height += self.element_spacing
        # buttons area
        if self.button_specs:
            button_height = 40
            # account for all stacked buttons: each button contributes its height
            # plus the spacing that follows it (render() advances cursor by button_height + spacing)
            popup_height += len(self.button_specs) * (button_height + self.element_spacing)
        # remove last extra spacing
        if popup_height > 0:
            popup_height -= self.element_spacing
        # add vertical padding
        popup_height += 2 * self.padding
        return popup_height

    def render(self, screen: pygame.Surface, button_manager: ButtonManager, center=True):
        """Render the popup and register buttons into the provided ButtonManager.

        Returns the popup rect.
        """
        self._ensure_fonts()
        # Draw overlay
        draw_overlay(screen, (0, 0, 0))

        popup_height = self.compute_height(screen)
        popup_width = self.popup_width
        if center:
            popup_x_pos, popup_y_pos = center_popup(screen.get_width(), screen.get_height(), popup_width, popup_height)
        else:
            # fallback to top-left
            popup_x_pos, popup_y_pos = (0, 0)

        # background
        draw_popup_background(screen, (255, 255, 255), popup_x_pos, popup_y_pos, popup_width, popup_height)

        # layout cursor
        layout_cursor_y = popup_y_pos + self.padding
        popup_center_x = popup_x_pos + popup_width // 2

        # title
        if self.title:
            title_surface = self.title_font_style.render(self.title, True, (0, 0, 0))
            title_rect = title_surface.get_rect(centerx=popup_center_x, top=layout_cursor_y)
            screen.blit(title_surface, title_rect)
            layout_cursor_y = title_rect.bottom + self.element_spacing

        # images
        for image in self.images:
            image_rect = image.get_rect(centerx=popup_center_x, top=layout_cursor_y)
            screen.blit(image, image_rect)
            layout_cursor_y = image_rect.bottom + self.element_spacing

        # body lines
        for line in self.body_lines:
            line_surface = self.body_font_style.render(line, True, (0, 0, 0))
            line_rect_obj = line_surface.get_rect(centerx=popup_center_x, top=layout_cursor_y)
            screen.blit(line_surface, line_rect_obj)
            layout_cursor_y = line_rect_obj.bottom + self.element_spacing

        # buttons
        # Clear previous buttons and add new ones centered horizontally stacked vertically
        button_manager.clear()
        if self.button_specs:
            button_width = min((popup_width - 2 * self.padding), 240)
            button_height = 40
            button_x_pos = popup_x_pos + (popup_width - button_width) // 2
            # place buttons with spacing
            for label, action, color in self.button_specs:
                button_manager.add_button(rect=(button_x_pos, layout_cursor_y, button_width, button_height), label=label, action=action, color=color, text_color=(255,255,255))
                layout_cursor_y += button_height + self.element_spacing

        # Draw buttons immediately so popup owns its visuals and cursor state
        button_font = pygame.font.SysFont('Arial', 18, bold=True)
        button_manager.draw(screen, button_font)
        button_manager.set_cursor()

        return pygame.Rect(popup_x_pos, popup_y_pos, popup_width, popup_height)
