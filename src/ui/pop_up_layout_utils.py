def center_popup(screen_width, screen_height, popup_width, popup_height):
    """Calculate centered position for a popup."""
    center_x_pos = (screen_width - popup_width) // 2
    center_y_pos = (screen_height - popup_height) // 2
    return center_x_pos, center_y_pos
