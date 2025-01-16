import pygame

from characters import Player


class Game:
    def __init__(self) -> None:
        WINDOW_WIDTH, WINDOW_HEIGHT = 256, 240
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.icon = pygame.image.load("data/run2.png")
        
        self.player = Player()
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("setup")
        
        self.game_loop()

    def game_loop(self) -> None:
        running = True
        
        while running:
            self.screen.fill((0, 0, 225))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move_player(speed=-5)
                    if event.key == pygame.K_RIGHT:
                        self.player.move_player(speed=5)
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.move_player(speed=0)

            self.player.render(screen=self.screen)
            print(self.player.get_position())
            
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
