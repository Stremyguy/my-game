import pygame

from characters import Player, FlyingVirus, RockSleeper
from levels import Level
from power_booster import PowerBooster
from instruments import load_image, load_font, load_music

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
        
        self.level_ids = [1, 2, 3]
        self.current_scene = 0
        self.is_game_over = False
        self.is_paused = False
        
        self.particles = pygame.sprite.Group()
        
        # fonts
        pygame.font.init()
        self.my_font = pygame.font.Font(load_font("PressStartFont.ttf"), 13)
        
        pygame.mixer.init()

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("setup")
        
        self.levels_setup()
        self.game_loop()
    
    def game_loop(self) -> None:
        self.running = True
        
        self.camera = Camera(
                level_width=self.current_level.width * self.current_level.tile_size,
                level_height=self.current_level.height * self.current_level.tile_size
            )
        
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            
            self.screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.pause_game()
                
                if self.current_scene in self.level_ids:
                    self.player_input(event)
            
            if self.current_scene in self.scenes:
                self.scenes[self.current_scene](dt, event)
        
            next_scene = self.current_level.check_scene_transition()
        
            if next_scene is not None and next_scene in self.levels:
                self.switch_scene(next_scene)
            
            if self.player.check_game_over():
                self.current_scene = 5
            
            # print(self.player.power_level)
            
            pygame.display.update()
            self.clock.tick(self.fps)
    
    def player_input(self, event) -> None:
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
    
    def draw_text(self, text: str, font: "pygame", text_color: tuple, x: int, y: int, align: str = "center") -> None:
        img = font.render(text, True, text_color)
        if align == "center":
            rect = img.get_rect(center=(x, y))
        elif align == "right":
            rect = img.get_rect(topright=(x, y))
        elif align == "left":
            rect = img.get_rect(topleft=(x, y))
            
        self.screen.blit(img, rect)
    
    def switch_scene(self, scene_id: int) -> None:
        if scene_id in self.scenes:
            self.current_scene = scene_id
            self.current_level = self.levels[scene_id]
            
            self.player.set_position(*self.current_level.player_position)
            
            self.camera = Camera(
                level_width=self.current_level.width * self.current_level.tile_size,
                level_height=self.current_level.height * self.current_level.tile_size
            )
    
    def pause_game(self) -> None:
        is_paused = True
        
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
    
    def main_menu(self, dt: float = None, event=None) -> None:
        self.screen.fill((0, 0, 0))
        self.screen.blit(load_image("virus.png"), (10, 10))
        
        self.draw_text(text="PRESS START!",
                       font=self.my_font,
                       text_color=(255, 255, 255),
                       x=WINDOW_WIDTH / 2,
                       y=180,
                       align="center")
        
        self.draw_text(text="@Stremyguy",
                       font=self.my_font,
                       text_color=(255, 255, 255),
                       x=WINDOW_WIDTH / 2,
                       y=210,
                       align="center")
        
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            self.current_scene = 1
                
        pygame.display.update()
        
    def level_1(self, dt: float, event=None) -> None:
        self.run_level(self.current_level, dt)
    
    def level_2(self, dt: float, event=None) -> None:
        self.run_level(self.current_level, dt)
    
    def level_3(self, dt: float, event=None) -> None:
        self.run_level(self.current_level, dt)
    
    def ending(self, dt=None, event=None) -> None:
        pass
    
    def game_over(self, dt=None, event=None) -> None:
        self.screen.fill((0, 0, 0))
        game_over_img = load_image("game_over.png")
        self.screen.blit(game_over_img, (0, WINDOW_HEIGHT // 2 - 50))
    
    def run_level(self, level: "Level", dt: float) -> None:
        self.camera.update(self.player)
        level.render(screen=self.screen, camera=self.camera)
                
        for enemy in level.enemies_sprites:
            enemy.update(screen=self.screen, camera=self.camera, player=self.player)

        for power_booster in level.power_boosters_sprites:
            power_booster.update(screen=self.screen, camera=self.camera, player=self.player)
        
        self.particles.update()
        self.particles.draw(self.screen)
        
        block_tiles = level.get_block_tiles()
        self.player.update(screen=self.screen, camera=self.camera, dt=dt, block_tiles=block_tiles, enemy_sprites=self.enemy_sprites, level=level)
        
        self.player_info()
    
    def levels_setup(self) -> None:
        self.enemy_sprites = pygame.sprite.Group()
        
        enemies = {
            1: [
                [RockSleeper(position=(50, 180), screen=self.screen)],
                [RockSleeper(position=(190, 180), screen=self.screen)],
                [RockSleeper(position=(443, 121), screen=self.screen)],],
            2: [
                [FlyingVirus(position=(100, 4), screen=self.screen)],
                [FlyingVirus(position=(300, 4), screen=self.screen)],
                [FlyingVirus(position=(400, 4), screen=self.screen)],
                [FlyingVirus(position=(500, 4), screen=self.screen)],
                [RockSleeper(position=(443, 180), screen=self.screen)],],
            3: [
                [],]
        }
        
        power_boosters = {
            1: [
                [(728, 160)],
                [(20, 10)],
                [(30, 10)],],
            2: [
                [(0, 10)],
                [(50, 10)],
                [(60, 10)],]
        }
        
        self.levels = {
            1: Level(
                level_name="level_1",
                player=self.player,
                player_position=(0, 180),
                enemies_data=enemies[1],
                power_boosters_data=power_boosters[1],
                music_theme="main theme.mp3",
                block_tiles_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 
                                29, 31, 32, 33, 34, 36, 37, 38, 39, 
                                40, 41, 50, 51, 52, 53, 54, 55, 56, 
                                58, 60, 61, 62, 63, 64, 65, 66, 67, 
                                68, 69, 70, 71, 72, 73, 74],
                transition_tiles_id=[35],
                next_scene_id=2
            ),
            2: Level(
                level_name="level_2",
                player=self.player,
                player_position=(0, 0),
                enemies_data=enemies[2],
                power_boosters_data=power_boosters[2],
                music_theme="theme test.wav",
                block_tiles_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 
                                29, 31, 32, 33, 34, 36, 37, 38, 39, 
                                40, 41, 50, 51, 52, 53, 54, 55, 56, 
                                58, 60, 61, 62, 63, 64, 65, 66, 67, 
                                68, 69, 70, 71, 72, 73, 74],
                transition_tiles_id=[35],
                next_scene_id=3
            ),
            3: Level(
                level_name="bossfight_1",
                player=self.player,
                player_position=(0, 0),
                enemies_data=enemies[3],
                power_boosters_data=power_boosters[1],
                music_theme="theme test.wav",
                block_tiles_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 
                                29, 31, 32, 33, 34, 36, 37, 38, 39, 
                                40, 41, 50, 51, 52, 53, 54, 55, 56, 
                                58, 60, 61, 62, 63, 64, 65, 66, 67, 
                                68, 69, 70, 71, 72, 73, 74],
                transition_tiles_id=[35],
                next_scene_id=1
            )
        }
        
        self.current_level = self.levels[1]
    
    def player_info(self) -> None:
        print(self.player.rect.x, self.player.rect.y)
        current_lvl_name = self.current_level.level_name.split("_")
        level_info = ""
        p_points_info = str(self.player.power_level)
        
        if "level" in current_lvl_name:
            level_info = f"Lvl: {current_lvl_name[1]}"
        elif "bossfight" in current_lvl_name:
            level_info = f"Bf: {current_lvl_name[1]}"
        
        self.draw_text(level_info, self.my_font, (255, 255, 255), 240, 10, "right")
        self.draw_text(p_points_info, self.my_font, (255, 255, 255), 240, 33, "right")


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
