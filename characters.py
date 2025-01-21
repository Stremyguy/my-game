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
        self.moving_y = False
        self.on_ground = False
        
        self.speed = 2
        self.gravity = 700
        self.jump_force = -300
        self.velocity_y = 0
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
    
    def move_player(self, speed: int = 2) -> None:
        if speed < 0:
            self.flip_x = True
        elif speed > 0:
            self.flip_x = False
        
        if self.moving_x is True:
            self.rect.x += speed
    
    def jump(self) -> None:
        if self.on_ground:
            self.rect.y -= 50
            self.on_ground = False
    
    def gravity_check(self, block_tiles: list) -> None:
        self.on_ground = False
        
        self.rect.y += 5
        
        for tile in block_tiles:
            if self.rect.colliderect(tile):
                if self.rect.bottom > tile.top and self.rect.bottom - 5 <= tile.top:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    break
                    
    def get_current_sprite(self) -> str:
        folder = "data/"
        
        if self.current_state == "run":
            return f"{folder}{self.sprites_states["run"][self.current_frame]}"
        
        return f"{folder}{self.sprites_states[self.current_state]}"
    
    def check_game_over(self) -> bool:
        if self.rect.y >= 240:
            return True
        
        return False
    
    def render(self, screen: "pygame", camera) -> None:
        current_sprite = pygame.image.load(self.get_current_sprite())
        current_sprite = pygame.transform.flip(current_sprite, self.flip_x, False)
        
        rect = self.rect.copy()
        camera.apply(rect)
        
        screen.blit(current_sprite, rect.topleft)
    
    def update(self, screen: "pygame", camera, dt: float, block_tiles: list) -> None:
        self.move_player(speed=self.speed)
        self.update_animation(dt)
        
        self.gravity_check(block_tiles)
        
        self.render(screen, camera=camera)


class Enemy:
    def __init__(self, enemy_code: int, position: tuple) -> None:
        self.enemy_code = enemy_code
        self.position = position

        self.setup()
    
    def setup(self) -> None:
        pass

