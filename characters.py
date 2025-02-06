import pygame
import math
import random

from instruments import load_image
from constants import *
from particles import ParticleManager


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
        
        # player parameters
        self.flip_x = False
        self.current_state = "idle"
        self.moving_x = False
        self.on_ground = False
        self.killed = False
        self.can_move = True

        # physics
        self.gravity = GRAVITY
        self.jump_force = 300
        self.y_velocity = 0
        
        self.speed = 0
        self.hp = 100
        self.power_level = 10
        self.player_score = 0
        
        self.ultra_piece_collected = False
    
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
    
    def update_score(self) -> None:
        self.player_score += 1
    
    def move_player(self, block_tiles: list) -> None:
        if self.can_move:
            if self.rect.x + self.speed < 0:
                self.rect.x = 0
            elif self.rect.x + self.rect.width + self.speed > 1200:
                self.rect.x = 1200 - self.rect.width
            else:
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
    
    def check_collisions(self, block_tiles: list, enemy_sprites: "pygame", dt: float) -> None:
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
        if self.rect.y >= 240 or self.power_level < 0 or self.hp <= 0:
            return True
        
        return False
    
    def shoot(self) -> None:
        pass
    
    def check_win(self) -> bool:
        if self.ultra_piece_collected:
            return True
        
        return False
    
    def render(self, screen: "pygame", camera) -> None:
        current_sprite = pygame.image.load(self.get_current_sprite())
        current_sprite = pygame.transform.flip(current_sprite, self.flip_x, False)
        
        rect = self.rect.copy()
        camera.apply(rect)
        
        screen.blit(current_sprite, rect.topleft)
    
    def update(self, screen: "pygame", camera, dt: float, block_tiles: list, enemy_sprites: "pygame", level) -> None:
        self.apply_gravity(dt)
        self.move_player(block_tiles)
        self.check_collisions(block_tiles, enemy_sprites, dt)
        self.update_animation(dt)
        self.update_score()
        self.render(screen, camera=camera)
        
        if level.check_scene_transition():
            return level.next_scene_id
        
        return None


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position: tuple, screen: "pygame") -> None:
        super().__init__()
        self.position = position
        self.screen = screen
        self.rect = None
    
    def set_pos(self, x: int = 0, y: int = 0) -> None:
        self.rect.x = x
        self.rect.y = y
        
    def render(self, camera) -> None:
        enemy_rect = self.rect.copy()
        camera.apply(enemy_rect)
        self.screen.blit(self.image, enemy_rect.topleft)
    
    # def render(self, camera) -> None:
    #     camera.apply(self.rect)
    #     self.screen.blit(self.image, self.rect.topleft)
    
    def update(self, camera, player) -> None:
        self.move()
        self.attack()
        self.check_collision(player)
        self.render(camera)


class FlyingVirus(Enemy):
    def __init__(self,
                 position: tuple = (0, 0),
                 screen: "pygame" = None) -> None:
        super().__init__(position, screen)
        self.x = position[0]
        self.y = position[1]
        self.start_x = position[0]
        self.start_y = position[1]
        
        self.image = load_image("enemy idle.png")
        self.rect = self.image.get_rect()
        
        self.speed = 2
        self.amplitude = 100
        self.frequency = 0.1
        self.hit_force = 30
        self.level_width = 1200
        self.direction = 1
        self.screen = screen

        self.x_offset = 0
        self.time = 0
        self.attack_timer = 0
        
        self.circle_time = 0
        self.is_circle_attacking = False
        self.hit = False
        
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
            if not self.hit:
                player.power_level -= 1
                self.hit = True
                return True
        return False

    def update(self, screen: "pygame", camera, player) -> None:
        if self.is_circle_attacking:
            self.update_circle_movement()
        else:
            self.move()
        
        self.attack()
        self.check_collision(player)
        
        self.hit = False
        
        self.render(camera)


class RockSleeper(Enemy):
    def __init__(self, 
                 position: tuple = (0, 0),
                 screen: "pygame" = None) -> None:
        super().__init__(position, screen)
        self.x = position[0]
        self.y = position[1]
        self.start_x = position[0]
        self.start_y = position[1]
        
        self.hit_force = 30
        self.direction = 1
        self.level_width = 1200
        self.screen = screen
        
        self.attack_counter = 0
        
        self.attack_timer = 0
        self.sleep_timer = 0
        
        self.sprites_states = {
            "idle": "enemy_2_idle.png",
            "attack": "enemy_2_attack.png",
            "sleep": "enemy_2_sleep.png"
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
        self.attack_counter += 1
        
        bullet = Bullet(position=(self.rect.centerx, self.rect.bottom - 15),
                        speed=-10,
                        sprite_file="virus.png",
                        x_dir=True,
                        y_dir=False)
        
        self.bullets.add(bullet)
    
    def attack(self) -> None:
        if self.attack_counter <= 5:
            self.attack_timer += 1
            
            if self.attack_timer >= 50:
                self.set_state("attack")
                self.spawn_bullet()
                self.attack_timer = 0
            elif self.attack_timer >= 5:
                self.set_state("idle")
        else:
            self.sleep_timer += 1
            self.set_state("sleep")
            
            if self.sleep_timer >= 150:
                self.sleep_timer = 0
                self.attack_counter = 0
                self.attack()
    
    def check_collision(self, player) -> None:
        for bullet in self.bullets:
            if pygame.sprite.collide_rect(bullet, player) and not bullet.hit:
                player.power_level -= 1
                bullet.hit = True
                bullet.kill()
                return True
        return False
    
    def render(self, camera) -> None:
        enemy_rect = self.rect.copy()
        camera.apply(enemy_rect)
        self.screen.blit(self.image, enemy_rect.topleft)
        
        for bullet in self.bullets:
            bullet.render(self.screen, camera)

    def update(self, screen: "pygame", camera, player) -> None:
        self.attack()
        self.check_collision(player)
        self.render(camera)
        self.bullets.update()



class Boss(Enemy):
    def __init__(self, 
                 position: tuple = (0, 0),
                 screen: "pygame" = None) -> None:
        super().__init__(position, screen)
        self.x = position[0]
        self.y = position[1]
        self.start_x = position[0]
        self.start_y = position[1]
        
        self.speed = 2
        self.hit_force = 30
        self.direction = 1
        self.level_width = 1200
        self.screen = screen
        
        self.attack_counter = 0
        
        self.attack_timer = 0
        self.sleep_timer = 0
        
        self.sprites_states = {
            "idle": "boss.png",
            "attack": "boss.png",
            "sleep": "boss.png"
        }
        
        self.image = load_image("enemy_2_idle.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.bullets = pygame.sprite.Group()
        self.running_counter = 0
        self.set_pos(x=position[0], y=position[1])
            
    def set_pos(self, x: int = 0, y: int = 0) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def set_state(self, state: str) -> None:
        self.image = load_image(self.sprites_states[state])
    
    def spawn_bullet(self) -> None:
        self.attack_counter += 1
        
        for _ in range(10):
            speed = random.randrange(-20, 20)
            x_dir = random.choice([True, False])
            y_dir = random.choice([True, False])
            bullet = Bullet(position=(self.rect.centerx, self.rect.bottom - 15),
                        speed=speed,
                        sprite_file="boss bullet.png",
                        x_dir=x_dir,
                        y_dir=y_dir)
            self.bullets.add(bullet)
    
    # def move(self, player) -> None:
    #     player_x, player_y = player.rect.centerx, player.rect.centery
    #     boss_x, boss_y = self.rect.centerx, self.rect.centery
    
    #     if player_x > boss_x:
    #         self.rect.x += self.speed
    #     elif player_x < boss_x:
    #         self.rect.x -= self.speed
    
    def attack(self) -> None:
        if self.attack_counter <= 5:
            self.attack_timer += 1
            
            if self.attack_timer >= 50:
                self.set_state("attack")
                self.spawn_bullet()
                self.attack_timer = 0
            elif self.attack_timer >= 5:
                self.set_state("idle")
        else:
            self.sleep_timer += 1
            self.set_state("sleep")
            self.running_counter = 0
            
            if self.sleep_timer >= 150:
                self.sleep_timer = 0
                self.attack_counter = 0
                self.attack()
    
    def check_collision(self, player) -> None:
        if pygame.sprite.collide_rect(self, player):
            player.hp = 0
            return True
        else:
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(bullet, player) and not bullet.hit:
                    player.power_level -= 1
                    bullet.hit = True
                    bullet.kill()
                    return True
        return False
    
    def render(self, camera) -> None:
        enemy_rect = self.rect.copy()
        camera.apply(enemy_rect)
        self.screen.blit(self.image, enemy_rect.topleft)
        
        for bullet in self.bullets:
            bullet.render(self.screen, camera)

    def update(self, screen: "pygame", camera, player) -> None:
        self.attack()
        self.check_collision(player)
        # self.move(player)
        self.render(camera)
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
        self.hit = False
        
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
        bullet_rect = self.rect.copy()
        camera.apply(bullet_rect)
        screen.blit(self.image, bullet_rect.topleft)
    
    def update(self) -> None:
        self.move()
