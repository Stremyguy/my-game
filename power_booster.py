import pygame


class PowerBooster(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("data/power booster.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
    def set_pos(self, x: int = 0, y: int = 0) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def set_sprite(self, sprite: str) -> None:
        self.image = pygame.image.load(f"data/{sprite}")
    
    def update(self) -> None:
        pass
