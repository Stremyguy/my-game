import pygame
from instruments import load_image


class ClassicPower(pygame.sprite.Sprite):
    def __init__(self, 
                 position: tuple = (0, 0), 
                 sprite: str = "power booster.png",
                 ) -> None:
        super().__init__()
        self.image = load_image(sprite)
        self.rect = self.image.get_rect()
        
        self.set_pos(x=position[0], y=position[1])
        
    def set_pos(self, x: int = 0, y: int = 0) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def set_sprite(self, sprite: str) -> None:
        self.image = load_image(sprite)
    
    def check_collision(self, player) -> None:
        pass
    
    def render(self, screen: "pygame", camera) -> None:
        booster_rect = self.rect.copy()
        camera.apply(booster_rect)
        screen.blit(self.image, booster_rect.topleft)
    
    def update(self, screen: "pygame", camera, player) -> None:
        self.render(screen, camera)
        self.check_collision(player)


class PowerBooster(ClassicPower):
    def __init__(self, 
                 position: tuple = (0, 0), 
                 sprite: str = "power booster.png",
                 ) -> None:
        super().__init__(position, sprite)
        
    def check_collision(self, player) -> None:
        if pygame.sprite.collide_rect(self, player):
            player.power_level += 1
            self.kill()


class PowerPiece(ClassicPower):
    def __init__(self, 
                 position: tuple = (0, 0), 
                 sprite: str = "power piece.png",
                 ) -> None:
        super().__init__(position, sprite)
        self.image = load_image(sprite)
        self.rect = self.image.get_rect()
        
        self.set_pos(x=position[0], y=position[1])

    def check_collision(self, player) -> None:
        if pygame.sprite.collide_rect(self, player):
            player.ultra_piece_collected = True
            self.kill()
