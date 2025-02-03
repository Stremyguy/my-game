import pygame
import random


class Particle(pygame.sprite.Sprite):
    def __init__(self, 
                 position: tuple,
                 velocity: tuple,
                 size: int,
                 color: tuple,
                 duration: float
                 ) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        
        self.velocity = velocity
        self.duration = duration
        self.elapsed_time = 0
        
    def update(self, dt: float, camera) -> None:
        self.elapsed_time += dt
        
        if self.elapsed_time > self.duration:
            self.kill()
        else:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            camera.apply(self.rect)


class Explosion(Particle):
    def __init__(self, 
                 position: tuple,
                 ) -> None:
        super().__init__(
            position=position,
            velocity=(random.uniform(-2, 2), random.uniform(-2, 2)),
            size=random.randint(4, 8),
            color=(255, random.randint(50, 150), 0),
            duration=random.uniform(0.4, 0.8)
        )


class ParticleManager(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
    
    def create_explosion(self, position: tuple) -> None:
        for _ in range(10):
            self.add(Explosion(position))


class Firework(Particle):
    def __init__(self, 
                 position: tuple,
                 size: int,
                 color: tuple,
                 duration: int
                 ) -> None:
        super().__init__(position, size, color, duration, fade_effects=True, color_effects=True)
        angle = random.uniform(0, 360)
        speed = random.uniform(3, 6)
        self.velocity = pygame.Vector2(speed, 0).rotate(angle)
    
    def update(self) -> None:
        super().update()
        self.position += self.velocity
        self.velocity.y += 0.1


class MagicOrb(Particle):
    def __init__(self, 
                 position: tuple,
                 size: int,
                 color: tuple,
                 duration: int
                 ) -> None:
        super().__init__(position, size, color, duration, color_effects=True)
        self.angle = random.uniform(0, 360)
        self.radius = random.uniform(5, 15)
    
    def update(self) -> None:
        super().update()
        self.angle += 5
        self.position.x += self.radius * 0.1 * pygame.math.cos(self.angle)
        self.position.y += self.radius * 0.1 * pygame.math.sin(self.angle)
