import pygame

from data.code.characters import Player
from data.code.levels import Level
from data.code.instruments import load_image, load_font, load_db, init_music, play_music, stop_music, play_sound
from data.code.constants import *
from data.code.db_handler import load_characters_from_db


# The main class for the game
class Game:
    def __init__(self) -> None:
        # constants setup
        self.fps = FPS
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.icon = load_image("run2.png")
        self.clock = pygame.time.Clock()
        self.player = Player()
        
        self.scenes = {
            0: self.main_menu,
            1: self.game_level,
            2: self.game_level,
            3: self.game_level,
            4: self.ending,
            5: self.game_over
        }
        
        self.level_ids = [1, 2, 3]
        self.current_scene = 0
        self.is_paused = False
        
        # game over stuff
        self.game_over_played = False
        self.game_over_counter = 0
        
        # winning stuff
        self.win_played = False
        self.win_counter = 0
        
        self.enemies = load_characters_from_db(load_db("characters.sqlite3"), self.screen)

        # fonts
        pygame.font.init()
        self.my_font = pygame.font.Font(load_font("PressStartFont.ttf"), 13)
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Jayver")
        
        init_music()
        self.levels_setup()
        self.game_loop()
    
    # game loop
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
        
            next_scene = None
        
            if self.current_scene in self.level_ids:
                next_scene = self.current_level.check_scene_transition()

            if next_scene is not None:
                self.switch_scene(next_scene)
            
            if self.player.check_game_over():
                self.switch_scene(5)
            elif self.player.check_win():
                self.switch_scene(4)
            
            self.check_score()
            
            pygame.display.update()
            self.clock.tick(self.fps)
    
    # player movement
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
    
    # a useful method for displaying text
    def draw_text(self, text: str, font: "pygame", text_color: tuple, x: int, y: int, align: str = "center") -> None:
        img = font.render(text, True, text_color)
        if align == "center":
            rect = img.get_rect(center=(x, y))
        elif align == "right":
            rect = img.get_rect(topright=(x, y))
        elif align == "left":
            rect = img.get_rect(topleft=(x, y))
            
        self.screen.blit(img, rect)
    
    # scene switching
    def switch_scene(self, scene_id: int) -> None:
        if scene_id in self.scenes:
            self.player.player_score = 0
            self.current_scene = scene_id
            
            if scene_id in self.level_ids:
                self.current_level = self.levels[scene_id]
                self.player.set_position(*self.current_level.player_position)
                self.camera = Camera(
                    level_width=self.current_level.width * self.current_level.tile_size,
                    level_height=self.current_level.height * self.current_level.tile_size
                )
                
                stop_music()
                play_music(self.current_level.music_theme)
    
    # pausing game
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
    
    # main menu scene
    def main_menu(self, dt: float = None, event=None) -> None:
        stop_music()
        play_music("main theme.mp3")
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(load_image("logo.png"), (0, 50))
        
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
    
    # running a level
    def game_level(self, dt: float, event=None) -> None:
        self.run_level(self.current_level, dt)
    
    # ending scene
    def ending(self, dt=None, event=None) -> None:
        if not self.win_played:
            stop_music()
            play_sound("win.mp3")
            self.win_played = True
        
        self.win_counter += dt
        win_img = load_image("you_win.png")
        
        if self.win_counter < 3:
            self.screen.fill((0, 0, 0))
            self.screen.blit(win_img, (0, WINDOW_HEIGHT // 2 - 50))
        else:
            self.screen.fill((0, 0, 0))
        
        self.draw_text(text=f"Your score: {self.player.final_score}",
                       font=self.my_font,
                       text_color=(255, 255, 255),
                       x=WINDOW_WIDTH / 2,
                       y=180,
                       align="center")
        
        pygame.display.update()
    
    # game over scene
    def game_over(self, dt=None, event=None) -> None:
        if not self.game_over_played:
            stop_music()
            play_sound("game_over.mp3")
            self.game_over_played = True
        
        self.game_over_counter += dt
        game_over_img = load_image("game_over.png")
        
        if self.game_over_counter < 3:
            self.screen.fill((0, 0, 0))
            self.screen.blit(game_over_img, (0, WINDOW_HEIGHT // 2 - 50))
        else:
            self.screen.fill((0, 0, 0))
        
        pygame.display.update()

    def run_level(self, level: "Level", dt: float) -> None:
        self.camera.update(self.player)
        level.render(screen=self.screen, camera=self.camera)
        enemy_objects = []
                       
        for enemy in level.enemies_sprites:
            enemy.update(screen=self.screen, camera=self.camera, player=self.player)

        for power_booster in level.power_boosters_sprites:
            power_booster.update(screen=self.screen, camera=self.camera, player=self.player)
        
        for power_piece in level.power_pieces_sprites:
            power_piece.update(screen=self.screen, camera=self.camera, player=self.player)
        
        block_tiles = level.get_block_tiles()
        
        for value in self.enemies.values():
            enemy_objects.append(value)
        
        self.player.update(screen=self.screen, camera=self.camera, dt=dt, block_tiles=block_tiles, enemy_sprites=self.enemy_sprites, level=level)
        
        self.player_info()
    
    def levels_setup(self) -> None:
        self.enemy_sprites = pygame.sprite.Group()
        
        power_boosters = {
            1: [
                [(728, 160)],
                [(384, 168)],
                [(944, 50)],],
            2: [
                [(834, 108)],
                [(594, 48)],
                [(414, 90)],]
        }
        
        power_piece = {
            3: [
                [(1138, 156)]
            ]
        }
        
        self.levels = {
            1: Level(
                level_name="level_1",
                player=self.player,
                player_position=(0, 180),
                enemies_data=self.enemies[1],
                power_boosters_data=power_boosters[1],
                power_pieces_data=None,
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
                enemies_data=self.enemies[2],
                power_boosters_data=power_boosters[2],
                power_pieces_data=None,
                music_theme="ud_theme.mp3",
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
                enemies_data=self.enemies[3],
                power_boosters_data=None,
                power_pieces_data=power_piece[3],
                music_theme="epic_boss_fight.mp3",
                block_tiles_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 
                                29, 31, 32, 33, 34, 36, 37, 38, 39, 
                                40, 41, 50, 51, 52, 53, 54, 55, 56, 
                                58, 60, 61, 62, 63, 64, 65, 66, 67, 
                                68, 69, 70, 71, 72, 73, 74],
                transition_tiles_id=[35],
                next_scene_id=4
            )
        }
        
        self.current_level = self.levels[1]
    
    def check_score(self) -> bool:
        if self.player.player_score > self.current_level.max_score:
            self.player.hp = 0
    
    def player_info(self) -> None:
        current_lvl_name = self.current_level.level_name.split("_")
        level_info = ""
        p_points_info = str(self.player.power_level)
        score_info = f"Score: {str(self.player.player_score)}"
        
        if "level" in current_lvl_name:
            level_info = f"Lvl: {current_lvl_name[1]}"
        elif "bossfight" in current_lvl_name:
            level_info = f"Bf: {current_lvl_name[1]}"
        
        self.draw_text(score_info, self.my_font, (255, 255, 255), 240, 10, "right")
        self.draw_text(level_info, self.my_font, (255, 255, 255), 240, 33, "right")
        self.draw_text(p_points_info, self.my_font, (255, 255, 255), 240, 56, "right")


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
