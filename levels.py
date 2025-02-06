from characters import Player
from power_booster import PowerBooster, PowerPiece
from instruments import load_level

import pygame


class Level:
    def __init__(self,
                 level_name: str,
                 player: "Player",
                 player_position: tuple,
                 enemies_data: list,
                 power_boosters_data: list,
                 power_pieces_data: list,
                 music_theme: str,
                 block_tiles_id: list,
                 transition_tiles_id: dict,
                 next_scene_id: int
                 ) -> None:
        self.level_name = level_name
        self.player = player
        self.player_position = player_position
        self.enemies_data = enemies_data
        self.power_boosters_data = power_boosters_data
        self.power_pieces_data = power_pieces_data
        self.music_theme = music_theme
        self.block_tiles_id = block_tiles_id
        self.transition_tiles_id = transition_tiles_id
        self.next_scene_id = next_scene_id
        
        self.map = load_level(self.level_name)
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        
        self.max_score = 10000
        
        self.setup()
    
    def setup(self) -> None:
        self.player.set_position(self.player_position[0], self.player_position[1])
        
        self.power_boosters_sprites = pygame.sprite.Group()
        self.power_pieces_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.bullets_sprites = pygame.sprite.Group()
        
        for enemy in self.enemies_data:
            enemy_sprite = enemy
            self.enemies_sprites.add(enemy_sprite)
        
        if self.power_boosters_data is not None:
            for power_booster in self.power_boosters_data:
                pos = power_booster[0]
                curr_power_booster = PowerBooster(position=pos)
                self.power_boosters_sprites.add(curr_power_booster)
        
        if self.power_pieces_data is not None:
            for power_piece in self.power_pieces_data:
                pos = power_piece[0]
                curr_power_piece = PowerPiece(position=pos)
                self.power_pieces_sprites.add(curr_power_piece)

    def get_block_tiles(self) -> list:
        block_tiles = []
        
        for y in range(self.height):
            for x in range(self.width):
                gid = self.map.get_tile_gid(x, y, 0)
                
                if gid:
                    props = self.map.tile_properties.get(gid, {})
                    
                    tile_id = props.get("id")
                    
                    if tile_id in self.block_tiles_id:
                        block_tiles.append(
                            pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                        )
        
        return block_tiles
    
    def get_transition_tiles(self) -> list:
        transition_tiles = []
        
        for y in range(self.height):
            for x in range(self.width):
                gid = self.map.get_tile_gid(x, y, 0)
                
                if gid:
                    props = self.map.tile_properties.get(gid, {})
                    
                    tile_id = props.get("id")
                    
                    if tile_id in self.transition_tiles_id:
                        transition_tiles.append(
                            pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                        )
        
        return transition_tiles
    
    def check_scene_transition(self) -> bool:
        for tile in self.get_transition_tiles():
            if self.player.rect.colliderect(tile):
                return self.next_scene_id
        
        return None
    
    def render(self, screen: "pygame", camera) -> None:
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                
                if image:
                    tile_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    camera.apply(tile_rect)
                    screen.blit(image, tile_rect.topleft)
                    