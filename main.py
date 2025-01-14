import pygame


class Game:
    def __init__(self) -> None:
        WINDOW_WIDTH, WINDOW_HEIGHT = 256, 240
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("setup")
        
        self.game_loop()
    
    def game_loop(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
