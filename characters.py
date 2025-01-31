import pygame
import math
import random

from instruments import load_image
from particles import create_particles, particles_group


class Player:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, 24, 24)
    
        self.sprites_states = {
            "idle": "idle main.png",
            "run": ["run1.png", "run2.png"],
        }
        
        # animation
        self.current_frame = 0
        self.animation_speed = 0.09
        self.frame_timer = 0
        
        self.flip_x = False
        self.current_state = "idle"
        self.moving_x = False
        self.on_ground = False
        self.killed = False
        self.can_move = True

        self.gravity = 1000
        self.jump_force = 300
        self.y_velocity = 0
        
        self.speed = 0
        
        self.hp = 100
        self.power_level = 0
        self.power_points_collected = 0
    
    def set_position(self, x: int, y: int) -> None:
        self.rect.topleft = (x, y)

    def set_speed(self, speed: int) -> None:
        self.speed = speed
    
    def update_animation(self, dt: float) -> None:
        if self.can_move:
            if self.current_state == "run" and self.moving_x:
                self.frame_timer += dt
                if self.frame_timer >= self.animation_speed:
                    self.current_frame = (self.current_frame + 1) % len(self.sprites_states["run"])
                    self.frame_timer = 0
    
    def move_player(self, block_tiles: list) -> None:
        if self.can_move:
            self.rect.x += self.speed
            
            for tile in block_tiles:
                if self.rect.colliderect(tile):
                    if self.speed > 0:
                        self.rect.right = tile.left
                    elif self.speed < 0:
                        self.rect.left = tile.right
    
    def jump(self) -> None:
        if self.on_ground:
            self.y_velocity = -self.jump_force
            self.on_ground = False
    
    def apply_gravity(self, dt: float) -> None:
        self.y_velocity += self.gravity * dt
        terminal_velocity = 800
        self.y_velocity = min(self.y_velocity, terminal_velocity)
    
    def check_collisions(self, block_tiles: list, dt: float) -> None:
        self.rect.y += self.y_velocity * dt
        
        for tile in block_tiles:
            if self.rect.colliderect(tile):
                if self.y_velocity > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    self.y_velocity = 0
                elif self.y_velocity < 0:
                    self.rect.top = tile.bottom
                    self.y_velocity = 0
        
    def get_current_sprite(self) -> str:
        folder = "data/"
        
        if self.current_state == "run":
            return f"{folder}{self.sprites_states["run"][self.current_frame]}"
        
        return f"{folder}{self.sprites_states[self.current_state]}"
    
    def check_game_over(self) -> bool:            
        if self.rect.y >= 240 or self.killed or self.hp <= 0:
            return True
        
        return False
    
    def render(self, screen: "pygame", camera) -> None:
        current_sprite = pygame.image.load(self.get_current_sprite())
        current_sprite = pygame.transform.flip(current_sprite, self.flip_x, False)
        
        rect = self.rect.copy()
        camera.apply(rect)
        
        screen.blit(current_sprite, rect.topleft)
    
    def update(self, screen: "pygame", camera, dt: float, block_tiles: list) -> None:
        self.apply_gravity(dt)
        self.move_player(block_tiles)
        self.check_collisions(block_tiles, dt)
        self.update_animation(dt)
        self.render(screen, camera=camera)


class Enemy:
    def __init__(self, position: tuple) -> None:
        self.position = position


class FlyingVirus(pygame.sprite.Sprite):
    def __init__(self, 
                 position: tuple, 
                 speed: float,
                 amplitude: int, 
                 frequency: float,
                 hit_force: int, 
                 level_width: int, 
                 screen: "pygame") -> None:
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        self.start_x = position[0]
        self.start_y = position[1]
        
        self.speed = speed
        self.amplitude = amplitude
        self.frequency = frequency
        self.hit_force = hit_force
        self.direction = 1
        self.level_width = level_width
        self.screen = screen
        
        self.image = load_image("enemy idle.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.x_offset = 0
        self.time = 0
        self.attack_timer = 0
        
        self.circle_time = 0
        self.is_circle_attacking = False
        # self.bullets = pygame.sprite.Group()
        
        self.linear_moves_needed = random.randint(5, 10)
        self.linear_moves_done = 0
        
        self.set_pos(x=position[0], y=position[1])
    
    def move(self) -> None:
        if not self.is_circle_attacking:
            self.time += 1
            self.x += self.speed * self.direction
            
            if self.x >= self.start_x + 40:
                self.direction = -1
                self.linear_moves_done += 1
            elif self.x <= self.start_x:
                self.direction = 1
                self.linear_moves_done += 1
            
            self.x = max(0, min(self.x, self.level_width - self.rect.width))
            self.set_pos(x=self.x, y=self.y)
            
    def set_pos(self, x: int = 0, y: int = 0) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def circle_attack(self) -> None:
        if not self.is_circle_attacking:
            self.is_circle_attacking = True
            self.circle_time = 0
    
    def update_circle_movement(self) -> None:
        if self.is_circle_attacking:
            self.circle_time += 15
            attack_radius = 60
            
            angle_rad = math.radians(self.circle_time)
            
            circle_center_y = self.start_y + attack_radius
            
            self.x = self.start_x + attack_radius * math.cos(angle_rad)
            self.y = circle_center_y - attack_radius * math.sin(angle_rad)
            
            if self.circle_time >= 360:
                self.is_circle_attacking = False
                self.circle_time = 0
                self.x = self.start_x
                self.y = self.start_y
                
            self.set_pos(x=self.x, y=self.y)
    
    # def spawn_bullet(self) -> None:
    #     bullet = Bullet(position=(self.rect.centerx, self.rect.bottom),
    #                     speed=10,
    #                     sprite_file="virus.png",
    #                     x_dir=False,
    #                     y_dir=True)
        
    #     self.bullets.add(bullet)
        
    def attack(self) -> None:
        self.attack_timer += 1
        
        if self.attack_timer >= 50:
            if self.linear_moves_done >= self.linear_moves_needed:
                self.circle_attack()
                self.attack_timer = 0
                self.linear_moves_needed = random.randint(5, 10)
                self.linear_moves_done = 0
    
    def check_collision(self, player) -> None:
        if pygame.sprite.collide_rect(self, player):
            player.hp -= self.hit_force
            return True
        return False
    
    def render(self, camera) -> None:
        camera.apply(self.rect)
        self.screen.blit(self.image, self.rect.topleft)
        
        # for bullet in self.bullets:
        #     bullet.render(self.screen, camera)

    def update(self, screen: "pygame", camera, player) -> None:
        if self.is_circle_attacking:
            self.update_circle_movement()
        else:
            self.move()
        particles_group.update()
        
        self.attack()
        self.check_collision(player)
        self.render(camera)
        particles_group.draw(screen)
        
        # self.bullets.update()


class RockSleeper(pygame.sprite.Sprite):
    def __init__(self, 
                 position: tuple,
                 hit_force: int, 
                 level_width: int, 
                 screen: "pygame") -> None:
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        self.start_x = position[0]
        self.start_y = position[1]
        
        self.hit_force = hit_force
        self.direction = 1
        self.level_width = level_width
        self.screen = screen
        
        self.attack_timer = 0
        
        self.sprites_states = {
            "idle": "enemy_2_idle.png",
            "attack": "enemy_2_attack.png",
        }
        
        self.image = load_image("enemy_2_idle.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.bullets = pygame.sprite.Group()

        self.set_pos(x=position[0], y=position[1])
            
    def set_pos(self, x: int = 0, y: int = 0) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def set_state(self, state: str) -> None:
        self.image = load_image(self.sprites_states[state])
    
    def spawn_bullet(self) -> None:
        bullet = Bullet(position=(self.rect.centerx, self.rect.bottom - 15),
                        speed=-10,
                        sprite_file="virus.png",
                        x_dir=True,
                        y_dir=False)
        
        self.bullets.add(bullet)
    
    def attack(self) -> None:
        self.attack_timer += 1
        
        if self.attack_timer >= 50:
            self.set_state("attack")
            self.spawn_bullet()
            self.attack_timer = 0
        elif self.attack_timer >= 5:
            self.set_state("idle")
    
    def check_collision(self, player) -> None:
        for bullet in self.bullets:
            if pygame.sprite.collide_rect(bullet, player):
                player.hp -= self.hit_force
                return True
        return False
    
    def render(self, camera) -> None:
        camera.apply(self.rect)
        self.screen.blit(self.image, self.rect.topleft)
        
        for bullet in self.bullets:
            bullet.render(self.screen, camera)

    def update(self, screen: "pygame", camera, player) -> None:
        self.attack()
        self.check_collision(player)
        self.render(camera)
        
        print(f"{self.x}; {self.y}")
        
        self.bullets.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, 
                 position: tuple, 
                 speed: float, 
                 sprite_file: str, 
                 x_dir: bool = True, 
                 y_dir: bool = False,
                 ) -> None:
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        
        self.image = load_image(sprite_file)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.x_dir = x_dir
        self.y_dir = y_dir
        
        self.speed = speed
        
        self.set_pos(x=self.x, y=self.y)
    
    def move(self) -> None:
        if self.y_dir:
            self.rect.y += self.speed
        if self.x_dir:
            self.rect.x += self.speed
    
    def set_pos(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def render(self, screen: pygame.Surface, camera) -> None:
        camera.apply(self.rect)
        screen.blit(self.image, self.rect.topleft)
    
    def update(self) -> None:
        self.move()
