from characters import Player

import pytmx
import pygame


class Level:
    def __init__(self,
                 level_name: str,
                 player: "Player",
                 player_position: tuple,
                 enemies_data: list,
                 block_tiles_id: list
                 ) -> None:
        self.level_name = level_name
        self.player = player
        self.player_position = player_position
        self.enemies_data = enemies_data
        self.block_tiles_id = block_tiles_id
        
        self.map = pytmx.load_pygame(f"data/levels/maps/{level_name}.tmx")
        self.height = self.map.height
        self.width = self.map.width
        
        self.tile_size = self.map.tilewidth
        
        self.setup()
    
    def setup(self) -> None:
        self.player.set_position(self.player_position[0], self.player_position[1])

    def render(self, screen: "pygame", camera) -> None:
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                
                if image:
                    tile_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    camera.apply(tile_rect)
                    screen.blit(image, tile_rect.topleft)
