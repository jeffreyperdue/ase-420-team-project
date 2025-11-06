import pygame
from src.constants import WIDTH, SCREEN_SIZE, FPS, START_SCREEN, PLAYING, GAME_OVER
from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.view.pygame_renderer import PygameRenderer
from src.view.input import InputHandler
from src.utils.session_manager import SessionManager

def spawn_piece():
    """Simple function to spawn a new piece"""
    from src.constants import START_X, START_Y
    return Piece(START_X, START_Y)

def handle_button_click(pos, game):
    """Handle clicking of start screen buttons."""
    # Get screen dimensions for button positions
    screen_width = SCREEN_SIZE[0]
    screen_height = SCREEN_SIZE[1]
    
    # Button dimensions from renderer
    button_width = 200
    button_height = 40
    
    # Calculate popup dimensions
    popup_width = 400
    popup_height = 500
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    
    # Calculate button positions (must match renderer)
    button_x = screen_width//2 - button_width//2
    start_y = popup_y + popup_height - 120
    exit_y = popup_y + popup_height - 60
    
    # Check start button
    if (button_x <= pos[0] <= button_x + button_width and 
        start_y <= pos[1] <= start_y + button_height):
        return "START"
        
    # Check exit button
    if (button_x <= pos[0] <= button_x + button_width and 
        exit_y <= pos[1] <= exit_y + button_height):
        return "EXIT"
    
    return None

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris (Team Project)")
    clock = pygame.time.Clock()
    
    # Create components
    session = SessionManager()
    board = Board(lambda: Row(WIDTH))
    game = Game(board, spawn_piece, session)  # Just the game referee
    renderer = PygameRenderer(screen)
    input_handler = InputHandler()
    
    # Main application loop
    done = False
    while not done:
        events = pygame.event.get()
        intents = []
        
        # Event processing
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for button in renderer.button_manager.buttons:
                        if button.is_hovered(event.pos):
                            button.clicked = True
                    intent = renderer.button_manager.handle_click(event.pos)
                    if intent:
                        intents.append(intent)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in renderer.button_manager.buttons:
                    button.clicked = False
        
        # Add keyboard intents
        intents.extend(input_handler.get_intents(events))
            
        # Apply intents and update game
        game.apply(intents)
        
        if "EXIT" in intents:
            done = True

        if game.done:
            done = True
            
        # Only update gravity when playing
        if game._state == PLAYING:
            game.update()

        # Draw current state
        renderer.draw_board(board)  # Draw the board grid and filled cells
        
        # Draw game elements if not in start screen
        if game._state != START_SCREEN:
            if game.current_piece:  # Draw the currently falling piece
                renderer.draw_piece(game.current_piece)
            if game.next_piece:  # Draw the next piece preview
                renderer.draw_next_piece_preview(game.next_piece)
            renderer.draw_score(game.score, game.high_score)

        # Draw overlays based on game state
        if game._state == START_SCREEN:
            renderer.draw_start_screen()
        elif game._state == GAME_OVER:
            renderer.draw_game_over_screen()
            
        # Refresh display
        pygame.display.flip()
        
        # Cap frame rate
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()