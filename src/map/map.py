from src.map.generator import MapGenerator
from src.utilities.settings import *


class Map:
    def __init__(self, game):
        self.game = game
        #map_info = generator.generate_from_txt(game)
        map_info = MapGenerator.generate_from_numpy(game, MAP_TILE_H, MAP_TILE_W)
        self.tiles_dict = map_info.tile_dict

        self.tilewidth = map_info.width_in_tile_numbers
        self.tileheight = map_info.height_in_tile_numbers
        self.height = map_info.height_in_pix
        self.width = map_info.width_in_pix

    def draw(self):
        pass

    def update(self):
        pass


