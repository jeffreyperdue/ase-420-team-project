import pygame

async def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("Simple Test")
    clock = pygame.time.Clock()
    
    # Simple test - just draw a red rectangle
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # Clear screen
        screen.fill((0, 0, 0))  # Black background
        
        # Draw a red rectangle
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 200))
        
        pygame.display.flip()
        clock.tick(60)
        await pygame.time.wait(0)
    
    pygame.quit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
