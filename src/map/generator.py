from src.utilities.settings import *
from src.map.tile import Tile
from collections import namedtuple
import numpy as np
from skimage import filters
import pygame as pg


class MapGenerator:

    @staticmethod
    def generate_from_txt(game):
        file_path = os.path.join(FOLDER_RESOURCES, 'map_1.txt')
        data = []
        with open(file_path, 'rt') as f:
            for line in f:
                data.append(line)

        # TODO: wrong. height in pix is not N*y, because the tiles are shifted. Works so far.
        height_in_tiles_numbers = len(data)
        width_in_tiles_numbers = len(data[0])
        height_in_pix = height_in_tiles_numbers * TILEHEIGHT
        width_in_pix = width_in_tiles_numbers * TILEWIDTH

        tile_dict = {}
        for row, tiles in enumerate(data):
            for col, el in enumerate(tiles):
                if el == '1':
                    tile_type = 'land'
                elif el == '.':
                    tile_type = 'sea'
                # elif el == 'P':
                #     self.game.ship = Ship(self.game, row, col)
                else:
                    tile_type = 'sea'

                # generate a tile:
                tile_dict[str(row) + '.' + str(col)] = Tile(game, row, col, tile_type)

        MapInfo = namedtuple('MapInfo',
                             ['tile_dict', 'width_in_tile_numbers', 'height_in_tile_numbers',
                             'height_in_pix', 'width_in_pix'])

        map_info = MapInfo(tile_dict=tile_dict,
                           width_in_tile_numbers=width_in_tiles_numbers,
                           height_in_tile_numbers=height_in_tiles_numbers,
                           height_in_pix=height_in_pix,
                           width_in_pix=width_in_pix)
        return map_info

    @staticmethod
    def generate_from_numpy(game, rows, columns):
        land = MapGenerator.generate_land(rows, columns)
        mountains = MapGenerator.generate_land(rows, columns)

        # add mountains ONLY to the land:
        pixel_map = land + land * mountains

        height_in_tiles_numbers = rows
        width_in_tiles_numbers = columns
        height_in_pix = height_in_tiles_numbers * TILEHEIGHT
        width_in_pix = width_in_tiles_numbers * TILEWIDTH

        tile_dict = {}
        # the keys will be coordinates r.c (e.g. '1.2' or '23.49')
        for row in range(0, rows):
            for col in range(0, columns):
                el = pixel_map[row, col]
                if el == 0:
                    tile_type = 'sea'
                elif el == 1:
                    tile_type = 'land'
                elif el == 2:
                    tile_type = 'mountain'
                else:
                    print('Unknown tile index. Using "sea" instead.')
                    tile_type = 'sea'

                # generate a tile:
                tile_dict[str(row) + '.' + str(col)] = Tile(game, row, col, tile_type)

        MapInfo = namedtuple('MapInfo',
                             ['tile_dict', 'width_in_tile_numbers', 'height_in_tile_numbers',
                              'height_in_pix', 'width_in_pix'])

        map_info = MapInfo(tile_dict=tile_dict,
                           width_in_tile_numbers=width_in_tiles_numbers,
                           height_in_tile_numbers=height_in_tiles_numbers,
                           height_in_pix=height_in_pix,
                           width_in_pix=width_in_pix)
        return map_info

    @staticmethod
    def generate_land(height, width):
        # generate land map
        # land=1,  the sea=0:
        sea = np.zeros((height, width))

        n = 25 # number of seeds for land

        # to make it completely random (randomize randomizer :)):
        np.random.seed(np.random.randint(100))
        # or make it reproducible with fixed randomizer:
        # np.random.seed(1)

        # generate random x,y coordinates (columns, rows):
        columns = width * np.random.random((1, n))
        rows = height * np.random.random((1, n))

        # put these coordinates into the sea as 1s:
        sea[rows.astype(np.int), columns.astype(np.int)] = 1

        # dilate them:
        # filter_sigma = w / (4. * n)
        filter_sigma = 5
        land = filters.gaussian(sea, sigma=filter_sigma)

        # make it binary:
        land = np.array(land > 0.7 * land.mean(), dtype=np.uint8)
        return land

    @staticmethod
    def generate_mountains(height, width):
        # TODO: repetitive functions. can be generalized.
        # generate mountains map.
        sea = np.zeros((height, width))

        # number of seeds for mountains
        n = 15

        # to make it completely random (randomize randomizer :)):
        np.random.seed(np.random.randint(100))
        # or make it reproducible with fixed randomizer:
        # np.random.seed(5)

        # generate random x,y coordinates (columns, rows):
        columns = width * np.random.random((1, n))
        rows = height * np.random.random((1, n))

        # put these coordinates into the sea as 1s:
        sea[rows.astype(np.int), columns.astype(np.int)] = 1

        # dilate them:
        filter_sigma = 1
        mountains = filters.gaussian(sea, sigma=filter_sigma)
        # make it binary:
        mountains = np.array(mountains > 0.7 * mountains.mean(), dtype=np.uint8)

        return mountains

    @staticmethod
    def generate_minimap(tile_dict, rows, cols):
        rgb = np.zeros((cols, rows, 3), dtype=np.uint8)
        rgb[:, :, :] = [50, 80, 255] # all set to blue
        # populate colors:
        for k, tile in tile_dict.items():
            if tile.type == 'land':
                color = [0, 255, 0]
                rgb[tile.c, tile.r, :] = color
            elif tile.type == 'mountain':
                color = [120, 120, 120]
                rgb[tile.c, tile.r, :] = color
        mini_map = pg.surfarray.make_surface(rgb)
        return mini_map