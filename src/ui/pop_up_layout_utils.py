def center_popup(screen_width, screen_height, popup_width, popup_height):
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    return popup_x, popup_y

def content_area(popup_x, popup_y, popup_width, popup_height, padding):
    content_x = popup_x + padding
    content_y = popup_y + padding
    content_width = popup_width - 2 * padding
    content_height = popup_height - 2 * padding
    return content_x, content_y, content_width, content_height