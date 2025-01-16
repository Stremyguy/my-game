import pygame


class Player:
    def __init__(self) -> None:
        self.position = (0, 0)
    
        self.sprites_states = {
            "idle": "idle main.png",
            "run_1": "run1.png",
            "run_2": "run2.png",
        }
        
        self.flip_x = False
        
        self.current_state = "idle"
        
        self.power_points_collected = 0
    
    def set_position(self, x: int, y: int) -> None:
        self.position = (x, y)
    
    def get_position(self) -> None:
        return self.position
    
    def move_player(self, speed: int = 5) -> None:
        if speed == 0 and self.flip_x:
            self.flip_x = True
        elif speed == 0 and not self.flip_x:
            self.flip_x = False
        elif speed < 0:
            self.flip_x = True
        else:
            self.flip_x = False
        
        x, y = list(self.position)
        
        x += speed
        
        self.set_position(x=x, y=y)
    
    def get_current_sprite(self) -> str:
        folder = "data/"
        
        return f"{folder}{self.sprites_states[self.current_state]}"
    
    def render(self, screen: "pygame") -> None:
        current_sprite = pygame.image.load(self.get_current_sprite())
        current_sprite = pygame.transform.flip(current_sprite, self.flip_x, False)
        screen.blit(current_sprite, self.position)
