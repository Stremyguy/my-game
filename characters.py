import pygame


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

        self.gravity = 500
        self.jump_force = 250
        self.y_velocity = 0
        
        self.speed = 0
        
        self.hp = 100
        self.power_points_collected = 0
    
    def set_position(self, x: int, y: int) -> None:
        self.rect.topleft = (x, y)

    def set_speed(self, speed: int) -> None:
        self.speed = speed
    
    def update_animation(self, dt: float) -> None:
        if self.current_state == "run" and self.moving_x:
            self.frame_timer += dt
            if self.frame_timer >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.sprites_states["run"])
                self.frame_timer = 0
    
    def move_player(self, block_tiles: list) -> None:
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
        if self.rect.y >= 240 or self.killed:
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
    def __init__(self, enemy_code: int, position: tuple) -> None:
        self.enemy_code = enemy_code
        self.position = position

        self.setup()
    
    def setup(self) -> None:
        pass

