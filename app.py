import pygame
from src.constants import WIDTH, SCREEN_SIZE, FPS
from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.view.pygame_renderer import PygameRenderer
from src.view.input import InputHandler

def spawn_piece():
    """Simple function to spawn a new piece"""
    from src.constants import START_X, START_Y
    return Piece(START_X, START_Y)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris (Team Project)")
    clock = pygame.time.Clock()
    
    # Create components
    board = Board(lambda: Row(WIDTH))
    game = Game(board, spawn_piece)  # Just the game referee
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
        renderer.draw_board(game.board)
        renderer.draw_piece(game.current_piece)
        
        # Update screen
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()