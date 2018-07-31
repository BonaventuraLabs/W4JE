from src.map.map_generator import MapGenerator
from src.utilities.settings import *
import numpy as np
import pygame as pg


class Map:
    def __init__(self, game):
        self.game = game
        self.sprites_map = pg.sprite.Group()

        # TODO: wrong. height in pix is not N*y, because the tiles are shifted. Works so far.
        self.width_in_tiles = MAP_TILE_W
        self.height_in_tiles = MAP_TILE_H
        self.height = TILEHEIGHT * MAP_TILE_H
        self.width = TILEWIDTH * MAP_TILE_W
        self.tiles_dict = MapGenerator.generate_from_numpy(game, self.sprites_map, MAP_TILE_H, MAP_TILE_W)

        # calculate xy of tiles
        for k, tile in self.tiles_dict.items():
            tile.center = Map.rc_to_xy(tile.r, tile.c)
            tile.rect.center = tile.center

    def animate(self):
        pass

    def draw(self):
        for k, tile in self.tiles_dict.items():
            self.game.screen.blit(tile.image, self.game.camera.apply(tile))

    def get_clicked(self, map_xy):
        clicked_item = None
        for k, tile in self.tiles_dict.items():
            if tile.rect.collidepoint(map_xy):
                clicked_item = tile
                clicked_item.on_click()
                break
        return clicked_item



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
