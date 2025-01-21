import pygame

from characters import Player
from levels import Level

WINDOW_WIDTH, WINDOW_HEIGHT = 256, 240


class Game:
    def __init__(self) -> None:
        self.fps = 60
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.icon = pygame.image.load("data/run2.png")
        
        self.clock = pygame.time.Clock()
        
        self.player = Player()
        
        self.scenes = ["menu", "lvl1", "lvl2", "lvl3", "lvl4", "lvl5", "ending", "game_over"]
        self.current_scene = 0
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("setup")
        
        pygame.font.init()
        
        self.levels_setup()
        self.game_loop()
    
    def game_loop(self) -> None:
        running = True
        camera = Camera(level_width=self.level.width * self.level.tile_size,
                        level_height=self.level.height * self.level.tile_size)
        
        while running:
            self.screen.fill((0, 0, 225))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.moving_x = True
                        self.player.set_speed(-2)
                        self.player.current_state = "run"
                    if event.key == pygame.K_RIGHT:
                        self.player.moving_x = True
                        self.player.set_speed(2)
                        self.player.current_state = "run"
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.moving_x = False
                        self.player.set_speed(0)
                        self.player.current_state = "idle"
            
            camera.update(self.player)
            self.level.render(screen=self.screen, camera=camera)
            dt = self.clock.tick(self.fps) / 1000.0
            block_tiles = self.level.get_block_tiles()
            self.player.update(screen=self.screen, camera=camera, dt=dt, block_tiles=block_tiles)
            
            print(self.player.on_ground)
            
            self.player_info()
            
            if self.player.check_game_over():
                self.game_over()
            
            self.clock.tick(self.fps)
            
            pygame.display.update()
    
    def levels_setup(self) -> None:
        enemies = {
            1: [
                []
            ],
            2: [
                [],
            ],
            3: [
                [],
            ],
            4: [
                [],
            ],
            5: [
                [],
            ]
        }
        
        self.level = Level(
            level_name="level_1",
            player=self.player,
            player_position=(17, 0),
            enemies_data=enemies[1],
            block_tiles_id=[2, 3]
        )
    
    def set_background_music(self, music_fn: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(f"data/music/{music_fn}")
        pygame.mixer.music.play(-1,0.0)
        
    def player_info(self) -> None:
        my_font = pygame.font.SysFont("Comic Sans MS", 20)
        
        hp_text_surface = my_font.render(f"hp: {self.player.hp}", False, (0, 0, 0))
        p_points_text_surface = my_font.render(str(self.player.power_points_collected), False, (0, 0, 0))
        
        self.screen.blit(hp_text_surface, (185, 0))
        self.screen.blit(p_points_text_surface, (240, 23))
        
    def main_menu(self) -> None:
        self.set_background_music(music_fn="main theme.mp3")
        
    def game_over(self) -> None:
        game_over_img = pygame.image.load("data/enemy died.png")
        self.screen.blit(game_over_img, (0, 0))


class Camera:
    def __init__(self, level_width: int, level_height: int) -> None:
        self.dx = 0
        self.dy = 0
        self.level_width = level_width
        self.level_height = level_height
    
    def apply(self, rect: pygame.Rect) -> None:
        rect.x += self.dx
        rect.y += self.dy
    
    def update(self, target: pygame.sprite.Sprite) -> None:
        self.dx = -(target.rect.x + target.rect.width // 2 - WINDOW_WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.height // 2 - WINDOW_HEIGHT // 2)
        
        self.dx = min(0, max(self.dx, -(self.level_width - WINDOW_WIDTH)))
        self.dy = min(0, max(self.dy, -(self.level_height - WINDOW_HEIGHT)))


if __name__ == "__main__":
    game = Game()
