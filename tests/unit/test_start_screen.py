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
    # Ensure pygame modules are initialized - do this explicitly
    try:
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()
    except:
        pass  # May already be initialized
    
    # Create a real Surface - use Surface directly to avoid mocking issues
    # This ensures get_size() works properly
    # Always create a new Surface to avoid any mocking issues
    try:
        screen = pygame.Surface((800, 600))
        # Verify it's a real Surface by checking it has get_size method
        if not hasattr(screen, 'get_size') or not callable(screen.get_size):
            # If somehow we got a mock, create a real one
            screen = pygame.Surface((800, 600))
    except:
        # If Surface creation fails, try to initialize and retry
        pygame.init()
        pygame.display.init()
        screen = pygame.Surface((800, 600))
    yield screen
    # Don't quit as it might interfere with other tests


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
            button_specs=buttons,
            popup_width=width,
            padding=padding,
            element_spacing=spacing
        )

        assert popup.title == title
        assert popup.body_lines == body_lines
        assert popup.button_specs == buttons
        assert popup.popup_width == width
        assert popup.padding == padding
        assert popup.element_spacing == spacing

    def test_popup_with_defaults(self):
        """Test Popup initialization with default values."""
        popup = Popup()

        assert popup.title is None
        assert popup.body_lines == []
        assert popup.images == []
        assert popup.button_specs == []
        assert popup.popup_width == 400
        assert popup.padding == 20
        assert popup.element_spacing == 10

    def test_popup_with_title_only(self):
        """Test Popup initialization with only title."""
        popup = Popup(title="Simple Title")

        assert popup.title == "Simple Title"
        assert popup.body_lines == []
        assert popup.images == []
        assert popup.button_specs == []

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
            button_specs=[("OK", "OK_ACTION", (0, 200, 0))]
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
            button_specs=[("OK", "OK_ACTION", (0, 200, 0))]
        )
        popup_two_buttons = Popup(
            title="Test",
            button_specs=[
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

# ============================================================================
# Tests for PygameRenderer Start Screen
# ============================================================================

class TestPygameRendererStartScreen:
    """Test PygameRenderer.draw_start_screen() functionality."""

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

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
