import pygame

from characters import Player, FlyingVirus, RockSleeper
from levels import Level
from instruments import load_image

WINDOW_WIDTH, WINDOW_HEIGHT = 256, 240


class Game:
    def __init__(self) -> None:
        self.fps = 60
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.icon = load_image("run2.png")
        
        self.clock = pygame.time.Clock()
        
        self.player = Player()
        
        self.scenes = {
            0: self.main_menu,
            1: self.level_1,
            2: self.level_2,
            3: self.level_3,
            4: self.ending,
            5: self.game_over
        }
        self.current_scene = 1
        self.is_game_over = False
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("setup")
        
        pygame.font.init()
        
        self.levels_setup()
        self.game_loop()
    
    def switch_scene(self, scene_id: int) -> None:
        if scene_id in self.scenes:
            self.current_scene = scene_id
    
    def game_loop(self) -> None:
        running = True
        
        while running:
            self.screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.current_scene in self.scenes:
                self.scenes[self.current_scene]()
        
            pygame.display.update()
            self.clock.tick(self.fps)
        
    def main_menu(self) -> None:
        self.screen.fill((0, 0, 0))
        self.screen.blit(load_image("virus.png"), (10, 10))
    
    def level_1(self) -> None:
        self.run_level(self.current_level)
    
    def level_2(self) -> None:
        pass
    
    def level_3(self) -> None:
        pass
    
    def ending(self) -> None:
        pass
    
    def game_over(self) -> None:
        self.screen.fill((0, 0, 0))
        game_over_img = load_image("game_over.png")
        self.screen.blit(game_over_img, (0, WINDOW_HEIGHT // 2 - 50))
    
    def run_level(self, level: "Level") -> None:
        self.camera = Camera(level_width=self.current_level.width * self.current_level.tile_size,
                             level_height=self.current_level.height * self.current_level.tile_size)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.moving_x = True
                    self.player.flip_x = True
                    self.player.set_speed(-2)
                    self.player.current_state = "run"
                if event.key == pygame.K_RIGHT:
                    self.player.moving_x = True
                    self.player.flip_x = False
                    self.player.set_speed(2)
                    self.player.current_state = "run"
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.moving_x = False
                    self.player.set_speed(0)
                    self.player.current_state = "idle"

        self.camera.update(self.player)
        level.render(screen=self.screen, camera=self.camera)
            
        for enemy in level.enemies_sprites:
            enemy.update(screen=self.screen, camera=self.camera, player=self.player)
            
        dt = self.clock.tick(self.fps) / 1000.0
        block_tiles = level.get_block_tiles()
        self.player.update(screen=self.screen, camera=self.camera, dt=dt, block_tiles=block_tiles)

        self.player_info()
    
    def levels_setup(self) -> None:
        self.enemy_sprites = pygame.sprite.Group()
        
        enemies = {
            1: [
                [RockSleeper((50, 180), hit_force = 30, level_width=1200, screen=self.screen)],
                [RockSleeper((190, 180), hit_force = 30, level_width=1200, screen=self.screen)]],
            2: [
                [FlyingVirus((0, 4), speed=2, amplitude=100, frequency=0.1, hit_force = 30, level_width=1200, screen=self.screen)],
                [FlyingVirus((100, 4), speed=2, amplitude=100, frequency=0.1, hit_force = 30, level_width=1200, screen=self.screen)],
                [FlyingVirus((300, 4), speed=2, amplitude=100, frequency=0.1, hit_force = 30, level_width=1200, screen=self.screen)],
                [FlyingVirus((400, 4), speed=2, amplitude=100, frequency=0.1, hit_force = 30, level_width=1200, screen=self.screen)],
                [FlyingVirus((500, 4), speed=2, amplitude=100, frequency=0.1, hit_force = 30, level_width=1200, screen=self.screen)]],
            3: [
                [],]
        }
        
        for key in enemies.values():
            for enemy in key:
                self.enemy_sprites.add(enemy)
        
        power_boosters = {
            1: [[(10, 10), "power booster.png"],
                [(20, 20), "power booster.png"],
                [(30, 30), "power booster.png"]]
        }
        
        self.level_1 = Level(
            level_name="level_1",
            player=self.player,
            player_position=(0, 110),
            enemies_data=enemies[1],
            power_boosters_data=power_boosters[1],
            music_theme="theme test.wav",
            block_tiles_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                            14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                            25, 26, 27, 28, 29, 31, 32, 33, 34,
                            36, 37, 38, 39, 40, 41, 50, 51, 52, 53,
                            54, 55, 56, 58],
        )
        
        self.current_level = self.level_1
        
    def player_info(self) -> None:
        my_font = pygame.font.SysFont("Comic Sans MS", 20)
        
        hp_text_surface = my_font.render(f"hp: {self.player.hp}", False, (0, 0, 0))
        p_points_text_surface = my_font.render(str(self.player.power_points_collected), False, (0, 0, 0))
        
        self.screen.blit(hp_text_surface, (185, 0))
        self.screen.blit(p_points_text_surface, (240, 23))


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
