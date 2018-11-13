from src.map.map_generator import MapGenerator
from src.utilities.settings import *
import numpy as np
import pygame as pg
from src.map.tile_item import Fish


class Map:

    def __init__(self, game):
        self.game = game
        self.sprites_map = pg.sprite.Group()

        self.width_in_tiles = MAP_TILE_W
        self.height_in_tiles = MAP_TILE_H
        # height in pix is not N*tile_h, because the tiles are shifted. This is a good proxy:
        self.height_in_pix = (TILEHEIGHT / 2 * 3) * int(MAP_TILE_H/2)
        self.width_in_pix = TILEWIDTH * MAP_TILE_W

        # simple map with circular sea in the middle:
        #self.tiles_dict = MapGenerator.generate_circle_map(game, self.sprites_map, MAP_TILE_H, MAP_TILE_W)
        # map from txt
        self.tiles_dict = MapGenerator.generate_from_txt(game, self.sprites_map)
        self.sea_tiles = []

        # randomly generated map:
        # self.tiles_dict = MapGenerator.generate_from_numpy(game, self.sprites_map, MAP_TILE_H, MAP_TILE_W)

        # calculate xy of tiles
        for k, tile in self.tiles_dict.items():
            tile.center = Map.rc_to_xy(tile.r, tile.c)
            tile.rect.center = tile.center
            if tile.type == 'sea':
                self.sea_tiles.append(tile)

        # make list of spawn points (player may appear only on Coast tile.
        self.get_spawn_tiles()

    def animate(self):
        pass

    def draw(self):
        for k, tile in self.tiles_dict.items():
            tile.draw()

    def add_fish(self):
        tile = np.random.choice(self.sea_tiles)
        tile.items.append(Fish(self))

    def get_tile_by_rc(self, r, c):
        target_tile = None
        for k, tile in self.tiles_dict.items():
            if (r, c) == (tile.r, tile.c):
                target_tile = tile
                break
        if target_tile is None:
            # print('could not find tile with rc: %s, %s'%(r, c))
            pass
        return target_tile


    def get_clicked(self, map_xy):
        target_tile = None
        for k, tile in self.tiles_dict.items():
            if tile.rect.collidepoint(map_xy):
                target_tile = tile
                target_tile.on_click()
                break
        return target_tile

    def get_spawn_tiles(self):
        coast_tiles = []
        for k, tile in self.tiles_dict.items():
            if tile.type == 'sand':
                coast_tiles.append((tile.r, tile.c))
        self.spawn_tiles_list = coast_tiles

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
