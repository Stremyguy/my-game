import pygame
import random
from instruments import load_image

particles_group = pygame.sprite.Group()
screen_rect = (0, 0, 256, 240)
GRAVITY = 1000


class Particle(pygame.sprite.Sprite):
    def __init__(self, sprite: str, position: tuple, dx: int, dy: int) -> None:
        super().__init__(particles_group)
        
        self.sprites = [load_image(sprite)]
        
        for scale in (5, 10, 20):
            self.sprites.append(pygame.transform.scale(self.sprites[0], (scale, scale)))
        
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = position
        
        self.gravity = GRAVITY
        
    def update(self) -> None:
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(sprite: str, position: tuple, particle_count: int = 20) -> None:
    numbers = (-5, 6)
    
    for _ in range(particle_count):
        Particle(sprite, position, random.choice(numbers), random.choice(numbers))
