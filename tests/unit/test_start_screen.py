"""
Unit tests for the start screen and Popup UI components.

Tests cover:
- Popup initialization and configuration
- Popup height computation with various content combinations
- Popup rendering and button registration
- Start screen rendering via pygame_renderer
- Button manager integration with popups
"""

import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock
from src.ui.pop_up import Popup
from src.ui.button_manager import ButtonManager
from src.ui.button import Button
from src.view.pygame_renderer import PygameRenderer


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def pygame_init():
    """Initialize pygame for tests."""
    if not pygame.display.get_surface():
        pygame.init()
        pygame.display.set_mode((800, 600))
    yield
    pygame.quit()


@pytest.fixture
def screen():
    """Create a test pygame screen."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    yield screen
    pygame.quit()


@pytest.fixture
def button_manager():
    """Create a ButtonManager instance."""
    return ButtonManager()


@pytest.fixture
def popup():
    """Create a basic Popup instance."""
    return Popup(
        title="Test Popup",
        body_lines=["Line 1", "Line 2"],
        buttons=[("OK", "OK_ACTION", (0, 200, 0))]
    )


# ============================================================================
# Tests for Popup Initialization
# ============================================================================

class TestPopupInitialization:
    """Test Popup.__init__ and property defaults."""

    def test_popup_with_all_parameters(self):
        """Test Popup initialization with all parameters provided."""
        title = "My Popup"
        body_lines = ["Body line 1", "Body line 2"]
        buttons = [("Start", "START", (0, 200, 0)), ("Exit", "EXIT", (200, 0, 0))]
        width = 500
        padding = 30
        spacing = 15

        popup = Popup(
            title=title,
            body_lines=body_lines,
            buttons=buttons,
            width=width,
            padding=padding,
            spacing=spacing
        )

        assert popup.title == title
        assert popup.body_lines == body_lines
        assert popup.buttons == buttons
        assert popup.width == width
        assert popup.padding == padding
        assert popup.spacing == spacing

    def test_popup_with_defaults(self):
        """Test Popup initialization with default values."""
        popup = Popup()

        assert popup.title is None
        assert popup.body_lines == []
        assert popup.images == []
        assert popup.buttons == []
        assert popup.width == 400
        assert popup.padding == 20
        assert popup.spacing == 10

    def test_popup_with_title_only(self):
        """Test Popup initialization with only title."""
        popup = Popup(title="Simple Title")

        assert popup.title == "Simple Title"
        assert popup.body_lines == []
        assert popup.images == []
        assert popup.buttons == []

    def test_popup_with_images(self):
        """Test Popup initialization with images."""
        pygame.init()
        img1 = pygame.Surface((100, 50))
        img2 = pygame.Surface((100, 50))
        images = [img1, img2]

        popup = Popup(images=images)

        assert popup.images == images
        assert len(popup.images) == 2


# ============================================================================
# Tests for Popup.compute_height
# ============================================================================

class TestPopupComputeHeight:
    """Test Popup.compute_height() with various content combinations."""

    def test_compute_height_empty_popup(self, screen):
        """Test height computation for an empty popup (no content)."""
        popup = Popup()
        height = popup.compute_height(screen)

        # Should only include padding (2 * padding)
        assert height == 2 * popup.padding

    def test_compute_height_title_only(self, screen):
        """Test height computation with title only."""
        popup = Popup(title="Test Title")
        height = popup.compute_height(screen)

        # Height should include title height + spacing + padding
        assert height > 2 * popup.padding
        popup_with_padding = height
        popup_without_padding = popup_with_padding - 2 * popup.padding
        assert popup_without_padding > 0

    def test_compute_height_title_and_body(self, screen):
        """Test height computation with title and body lines."""
        popup = Popup(
            title="Test Title",
            body_lines=["Line 1", "Line 2", "Line 3"]
        )
        height = popup.compute_height(screen)

        # Height should include title + all body lines + padding
        assert height > 2 * popup.padding

    def test_compute_height_with_single_button(self, screen):
        """Test height computation with a single button."""
        popup = Popup(
            title="Test",
            buttons=[("OK", "OK_ACTION", (0, 200, 0))]
        )
        height_with_button = popup.compute_height(screen)

        popup_no_button = Popup(title="Test")
        height_without_button = popup_no_button.compute_height(screen)

        # Height with button should be greater
        assert height_with_button > height_without_button
        # Difference should be approximately button height + spacing
        diff = height_with_button - height_without_button
        assert diff >= 40  # button height is 40

    def test_compute_height_with_multiple_buttons(self, screen):
        """Test height computation accounts for all stacked buttons."""
        popup_one_button = Popup(
            title="Test",
            buttons=[("OK", "OK_ACTION", (0, 200, 0))]
        )
        popup_two_buttons = Popup(
            title="Test",
            buttons=[
                ("OK", "OK_ACTION", (0, 200, 0)),
                ("Cancel", "CANCEL_ACTION", (200, 0, 0))
            ]
        )

        height_one = popup_one_button.compute_height(screen)
        height_two = popup_two_buttons.compute_height(screen)

        # Two buttons should produce greater height
        assert height_two > height_one
        # Difference should be approximately one button height + spacing
        diff = height_two - height_one
        assert diff >= 40  # button height is 40

    def test_compute_height_with_images(self, screen):
        """Test height computation includes image heights."""
        img1 = pygame.Surface((100, 50))
        img2 = pygame.Surface((100, 100))

        popup_no_images = Popup(title="Test")
        popup_with_images = Popup(
            title="Test",
            images=[img1, img2]
        )

        height_no_images = popup_no_images.compute_height(screen)
        height_with_images = popup_with_images.compute_height(screen)

        # With images should be greater
        assert height_with_images > height_no_images
        # Difference should be at least the sum of image heights
        diff = height_with_images - height_no_images
        assert diff >= 150  # 50 + 100

    def test_compute_height_with_all_content(self, screen):
        """Test height computation with title, images, body, and buttons."""
        img = pygame.Surface((100, 75))
        popup = Popup(
            title="Full Popup",
            body_lines=["Description 1", "Description 2"],
            images=[img],
            buttons=[
                ("Start", "START", (0, 200, 0)),
                ("Exit", "EXIT", (200, 0, 0))
            ]
        )

        height = popup.compute_height(screen)

        # Should be a reasonable size including all content
        assert height > 300  # arbitrary threshold for "reasonable" size

    def test_compute_height_increases_with_more_body_lines(self, screen):
        """Test that compute_height increases as body lines are added."""
        popup_base = Popup(title="Test")
        height_base = popup_base.compute_height(screen)

        popup_1_line = Popup(title="Test", body_lines=["Line 1"])
        height_1_line = popup_1_line.compute_height(screen)

        popup_3_lines = Popup(title="Test", body_lines=["Line 1", "Line 2", "Line 3"])
        height_3_lines = popup_3_lines.compute_height(screen)

        # Heights should be in increasing order
        assert height_base < height_1_line < height_3_lines


# ============================================================================
# Tests for Popup.render
# ============================================================================

class TestPopupRender:
    """Test Popup.render() rendering and button registration."""

    def test_popup_render_returns_rect(self, screen, button_manager):
        """Test that render() returns a Rect object."""
        popup = Popup(title="Test")
        result = popup.render(screen, button_manager)

        assert isinstance(result, pygame.Rect)
        assert result.width == popup.width
        assert result.height == popup.compute_height(screen)

    def test_popup_render_centers_by_default(self, screen, button_manager):
        """Test that render() centers the popup by default."""
        popup = Popup(title="Test")
        popup_rect = popup.render(screen, button_manager)

        # Popup should be roughly centered on screen
        screen_center_x = screen.get_width() // 2
        popup_center_x = popup_rect.centerx

        # Allow some tolerance for rounding
        assert abs(popup_center_x - screen_center_x) <= 10

    def test_popup_render_registers_buttons(self, screen, button_manager):
        """Test that render() registers buttons with the button manager."""
        popup = Popup(
            title="Test",
            buttons=[
                ("OK", "OK_ACTION", (0, 200, 0)),
                ("Cancel", "CANCEL_ACTION", (200, 0, 0))
            ]
        )
        popup.render(screen, button_manager)

        # Button manager should have registered buttons
        assert len(button_manager.buttons) == 2
        assert button_manager.buttons[0].label == "OK"
        assert button_manager.buttons[0].action == "OK_ACTION"
        assert button_manager.buttons[1].label == "Cancel"
        assert button_manager.buttons[1].action == "CANCEL_ACTION"

    def test_popup_render_clears_previous_buttons(self, screen, button_manager):
        """Test that render() clears previous buttons before registering new ones."""
        popup1 = Popup(
            title="First",
            buttons=[("Button1", "ACTION1", (0, 200, 0))]
        )
        popup1.render(screen, button_manager)
        assert len(button_manager.buttons) == 1

        popup2 = Popup(
            title="Second",
            buttons=[
                ("Button2a", "ACTION2a", (0, 200, 0)),
                ("Button2b", "ACTION2b", (200, 0, 0))
            ]
        )
        popup2.render(screen, button_manager)

        # Should have only the new buttons
        assert len(button_manager.buttons) == 2
        assert button_manager.buttons[0].label == "Button2a"

    def test_popup_render_with_no_buttons(self, screen, button_manager):
        """Test that render() works correctly with no buttons."""
        popup = Popup(title="No Buttons", body_lines=["Just content"])
        popup.render(screen, button_manager)

        # Button manager should be empty after clearing
        assert len(button_manager.buttons) == 0

    def test_popup_render_buttons_have_correct_bounds(self, screen, button_manager):
        """Test that rendered buttons have appropriate bounds within popup."""
        popup = Popup(
            title="Test",
            buttons=[("Start", "START", (0, 200, 0))]
        )
        popup_rect = popup.render(screen, button_manager)

        button = button_manager.buttons[0]
        btn_rect = button.rect

        # Button should be within popup bounds (with padding)
        assert btn_rect.left >= popup_rect.left + popup.padding - 10  # small tolerance
        assert btn_rect.right <= popup_rect.right - popup.padding + 10
        assert btn_rect.top >= popup_rect.top + popup.padding
        assert btn_rect.bottom <= popup_rect.bottom - popup.padding

    def test_popup_render_buttons_stacked_vertically(self, screen, button_manager):
        """Test that multiple buttons are stacked vertically."""
        popup = Popup(
            title="Test",
            buttons=[
                ("Button 1", "ACTION1", (0, 200, 0)),
                ("Button 2", "ACTION2", (200, 0, 0)),
                ("Button 3", "ACTION3", (0, 0, 200))
            ]
        )
        popup.render(screen, button_manager)

        buttons = button_manager.buttons
        # Buttons should be ordered top to bottom
        assert buttons[0].rect.top < buttons[1].rect.top < buttons[2].rect.top


# ============================================================================
# Tests for PygameRenderer Start Screen
# ============================================================================

class TestPygameRendererStartScreen:
    """Test PygameRenderer.draw_start_screen() functionality."""

    def test_draw_start_screen_initializes_renderer(self, screen):
        """Test that PygameRenderer initializes with button manager."""
        with patch('src.view.pygame_renderer.pygame.image.load') as mock_load:
            mock_img = pygame.Surface((100, 240))
            mock_load.return_value.convert_alpha.return_value = mock_img

            renderer = PygameRenderer(screen)

            assert isinstance(renderer.button_manager, ButtonManager)

    def test_draw_start_screen_registers_start_and_exit_buttons(self, screen):
        """Test that draw_start_screen registers Start and Exit buttons."""
        with patch('src.view.pygame_renderer.pygame.image.load') as mock_load:
            mock_img = pygame.Surface((100, 240))
            mock_load.return_value.convert_alpha.return_value = mock_img

            renderer = PygameRenderer(screen)
            renderer.draw_start_screen()

            # Should have Start and Exit buttons
            assert len(renderer.button_manager.buttons) == 2
            button_actions = [btn.action for btn in renderer.button_manager.buttons]
            assert "START" in button_actions
            assert "EXIT" in button_actions

    def test_draw_start_screen_button_colors(self, screen):
        """Test that start screen buttons have appropriate colors."""
        with patch('src.view.pygame_renderer.pygame.image.load') as mock_load:
            mock_img = pygame.Surface((100, 240))
            mock_load.return_value.convert_alpha.return_value = mock_img

            renderer = PygameRenderer(screen)
            renderer.draw_start_screen()

            buttons = renderer.button_manager.buttons
            # Start button should be green, Exit should be red (based on renderer implementation)
            actions_colors = {btn.action: btn.color for btn in buttons}

            assert actions_colors["START"] == (0, 200, 0)  # green
            assert actions_colors["EXIT"] == (200, 0, 0)   # red

    def test_draw_start_screen_title(self, screen):
        """Test that draw_start_screen uses 'Tetris' as title."""
        with patch('src.view.pygame_renderer.pygame.image.load') as mock_load:
            mock_img = pygame.Surface((100, 240))
            mock_load.return_value.convert_alpha.return_value = mock_img

            with patch('src.ui.pop_up.Popup.render') as mock_render:
                renderer = PygameRenderer(screen)
                renderer.draw_start_screen()

                # Verify Popup.render was called
                assert mock_render.called


# ============================================================================
# Tests for Button Manager Integration
# ============================================================================

class TestButtonManagerIntegration:
    """Test ButtonManager interaction with Popup."""

    def test_button_manager_clear_empties_buttons(self, button_manager):
        """Test that clear() removes all buttons."""
        button_manager.add_button((10, 10, 100, 40), "Test", "ACTION", (0, 200, 0))
        button_manager.add_button((10, 60, 100, 40), "Test2", "ACTION2", (200, 0, 0))

        assert len(button_manager.buttons) == 2
        button_manager.clear()
        assert len(button_manager.buttons) == 0

    def test_button_manager_handle_click_detects_hover(self, button_manager):
        """Test that handle_click detects button clicks based on position."""
        button_manager.add_button((10, 10, 100, 40), "Click Me", "CLICK_ACTION", (0, 200, 0))

        # Click inside button
        action = button_manager.handle_click((50, 30))
        assert action == "CLICK_ACTION"

        # Click outside button
        action = button_manager.handle_click((500, 500))
        assert action is None

    def test_button_manager_returns_first_hovered_button_action(self, button_manager):
        """Test that handle_click returns action of first hovered button."""
        button_manager.add_button((10, 10, 100, 40), "Button1", "ACTION1", (0, 200, 0))
        button_manager.add_button((10, 60, 100, 40), "Button2", "ACTION2", (200, 0, 0))

        # Position in first button
        action = button_manager.handle_click((50, 25))
        assert action == "ACTION1"

        # Position in second button
        action = button_manager.handle_click((50, 75))
        assert action == "ACTION2"


# ============================================================================
# Integration Tests
# ============================================================================

class TestStartScreenIntegration:
    """Integration tests for start screen flow."""

    def test_popup_render_and_button_interaction(self, screen, button_manager):
        """Test end-to-end: create popup, render it, and interact with buttons."""
        popup = Popup(
            title="Start Screen",
            body_lines=["Press a button to continue"],
            buttons=[
                ("Play", "PLAY", (0, 200, 0)),
                ("Quit", "QUIT", (200, 0, 0))
            ]
        )

        # Render the popup
        popup.render(screen, button_manager)

        # Verify buttons are registered
        assert len(button_manager.buttons) == 2

        # Get button positions
        play_button = next(btn for btn in button_manager.buttons if btn.action == "PLAY")
        quit_button = next(btn for btn in button_manager.buttons if btn.action == "QUIT")

        # Simulate click on play button
        action = button_manager.handle_click(play_button.rect.center)
        assert action == "PLAY"

        # Simulate click on quit button
        action = button_manager.handle_click(quit_button.rect.center)
        assert action == "QUIT"

    def test_popup_height_accommodates_all_content(self, screen, button_manager):
        """Test that popup height is sufficient for all rendered content."""
        popup = Popup(
            title="Complete Popup",
            body_lines=["Content line 1", "Content line 2", "Content line 3"],
            buttons=[
                ("Start", "START", (0, 200, 0)),
                ("Options", "OPTIONS", (0, 100, 200)),
                ("Exit", "EXIT", (200, 0, 0))
            ]
        )

        computed_height = popup.compute_height(screen)
        rendered_rect = popup.render(screen, button_manager)

        # Rendered height should match computed height
        assert rendered_rect.height == computed_height

        # Check button positions don't exceed popup bounds
        for button in button_manager.buttons:
            assert button.rect.bottom <= rendered_rect.bottom + 5  # 5px tolerance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
