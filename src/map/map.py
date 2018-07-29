from src.map.map_generator import MapGenerator
from src.utilities.settings import *
import numpy as np


class Map:
    def __init__(self, game):
        self.game = game
        #map_info = generator.generate_from_txt(game)
        map_info = MapGenerator.generate_from_numpy(game, MAP_TILE_H, MAP_TILE_W)

        self.tilewidth = map_info.width_in_tile_numbers
        self.tileheight = map_info.height_in_tile_numbers
        self.height = map_info.height_in_pix
        self.width = map_info.width_in_pix

        self.tiles_dict = map_info.tile_dict
        self.get_tiles_xy()

    def draw(self):
        # TODO: decouple from game sprite group?
        for sprite in self.game.sprites_map:
            self.game.screen.blit(sprite.image, self.game.camera.apply(sprite))

    def update(self):
        pass

    def get_tiles_xy(self):
        for k, tile in self.tiles_dict.items():
            tile.center = Map.rc_to_xy(tile.r, tile.c)
            tile.rect.center = tile.center

    def get_clicked(self, map_xy):
        # clicked_item = None
        for k, tile in self.tiles_dict.items():
            if tile.rect.collidepoint(map_xy):
                clicked_item = tile
                clicked_item.on_click()
                break
        # return clicked_item



    @staticmethod
    def rc_to_xy(r, c):
        # size of the bounding box of a tile:
        rx = TILE_HEX_R * np.cos(np.pi / 6)
        ry = TILE_HEX_R

        # real coordinates on map;
        # shift to right each 2nd row
        if r % 2 == 0:
            x = c * 2 * rx
            y = r * 1.5 * ry
        else:
            x = c * 2 * rx + rx  # here we shift to right.
            y = r * 1.5 * ry

        return x, y
