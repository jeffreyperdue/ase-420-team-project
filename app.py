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
                    for manager in (renderer.button_manager, renderer.hud_button_manager):
                        for button in manager.buttons:
                            if button.is_hovered(event.pos):
                                button.clicked = True
                    intent = renderer.button_manager.handle_click(event.pos)
                    if not intent:
                        intent = renderer.hud_button_manager.handle_click(event.pos)
                    if intent:
                        intents.append(intent)
            elif event.type == pygame.MOUSEBUTTONUP:
                for manager in (renderer.button_manager, renderer.hud_button_manager):
                    for button in manager.buttons:
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

        # Draw ghost piece if playing and not paused
        if game._state == PLAYING and game.current_piece and not game.paused:
            renderer.draw_ghost_piece(board, game.current_piece)
        
        # Draw level info if playing
        if game._state == PLAYING:
            renderer.draw_level_info(game.level, game.lines_cleared, game.gravity_delay)

        # Draw overlays and HUD elements after core board rendering
        if game._state == START_SCREEN:
            renderer.draw_start_screen()
            renderer.clear_hud_buttons()
        elif game._state == GAME_OVER:
            renderer.draw_game_over_screen(score=game.score, high_score=game.high_score)
            renderer.clear_hud_buttons()
        elif game.paused:
            renderer.draw_pause_popup(score=game.score, high_score=game.high_score)
            renderer.clear_hud_buttons()
        else:
            renderer.clear_popup_buttons()
            renderer.draw_pause_button()
            
        # Refresh display
        pygame.display.flip()
        
        # Cap frame rate
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()