import pygame
from src.constants import WIDTH, SCREEN_SIZE, FPS
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
        
        # Quit check
        for event in events:
            if event.type == pygame.QUIT:
                done = True
        
        # Handle game over state
        if game.game_over:
            # Check for restart or quit input
            intents = input_handler.get_intents(events)
            if intents:
                if "RESTART" in intents:
                    # Reset game state
                    board = Board(lambda: Row(WIDTH))
                    game = Game(board, spawn_piece, session)
                    renderer = PygameRenderer(screen)
                elif "QUIT" in intents:
                    done = True
        else:
            # Normal game input processing
            if game.done:
                done = True
            
            # Process input
            intents = input_handler.get_intents(events)
            if intents:
                print("Intents:", intents)
                if "QUIT" in intents:
                    done = True
                game.apply(intents)  # Apply game rules
            
            # Update game state
            game.update()
        
        # Render
        if game.game_over:
            # Draw the board in the background (frozen state)
            renderer.draw_board(game.board)
            # Draw game over overlay
            renderer.draw_game_over_screen()
            renderer.draw_score(game.score, game.high_score) # Position will be calculated relative to board
        else:
            # Normal rendering
            renderer.draw_board(game.board)
            renderer.draw_piece(game.current_piece)
            renderer.draw_score(game.score, game.high_score) # Position will be calculated relative to board
            renderer.draw_next_piece_preview(game.next_piece)
        
        # Draw pause screen overlay if paused
        if game.paused:
            renderer.draw_pause_screen()
            renderer.draw_level_info(game.level, game.lines_cleared, game.gravity_delay)
        
        # Update screen
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()