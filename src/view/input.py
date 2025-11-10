import pygame

class InputHandler:

    def __init__(self):
        # Map pygame keys to intent strings
        self.key_map = {
            pygame.K_UP: "ROTATE",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_DOWN: "DOWN",
            pygame.K_SPACE: "DROP",
            pygame.K_RETURN: "START",
            # ESC will be handled specially to emit both QUIT and PAUSE intents
            pygame.K_ESCAPE: "QUIT",
            pygame.K_r: "RESTART",  # Add restart key
            # Add 'p' key for pause toggle
            pygame.K_p: "PAUSE",
        }

    def get_intents(self, events):
        intents = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_map:
                    intents.append(self.key_map[event.key])
                    # If ESC is pressed, also treat it as a pause toggle
                    if event.key == pygame.K_ESCAPE:
                        intents.append("PAUSE")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                intents.append("CLICK")
        return intents
