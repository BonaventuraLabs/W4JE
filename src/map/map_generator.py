from src.utilities.settings import *
from src.map.tile import Tile
import numpy as np
from skimage import filters, feature
import pygame as pg


class MapGenerator:

    @staticmethod
    def generate_from_numpy(game, sprites_group, rows, columns):

        land_bool_map = MapGenerator.generate_land(rows, columns)
        mountains_bool_map = MapGenerator.generate_mountains(rows, columns)
        coast_bool_map = feature.canny(255*np.array(land_bool_map, dtype=np.uint8))
        # the coastal line will be calculated as edges of land:
        # 255 is necessary, since the gradient 1->0 is too weak. 255->0 is stringer edge.

        number_map = np.zeros((rows, columns), dtype=np.uint8)
        number_map[land_bool_map] = TILE_TYPE_DICT['land']
        number_map[coast_bool_map] = TILE_TYPE_DICT['sand']
        number_map[mountains_bool_map] = TILE_TYPE_DICT['mountain']

        return MapGenerator.generate_tiles(game, sprites_group, number_map)

    @staticmethod
    def generate_tiles(game, sprites_group, number_map):
        tile_dict = {}
        for row in range(0, number_map.shape[0]):
            for col in range(0, number_map.shape[1]):
                el = number_map[row, col]
                tile_type = TILE_TYPE_DICT[el]
                # generate a tile:
                tile_dict[str(row) + '.' + str(col)] = Tile(game, sprites_group, row, col, tile_type)
        return tile_dict

    @staticmethod
    def generate_land(height, width):
        # generate land map
        # land=1,  the sea=0:
        zeros = np.zeros((height, width))

        n = 25  # number of seeds for land

        # to make it completely random (randomize randomizer :)):
        np.random.seed(np.random.randint(100))
        # or make it reproducible with fixed randomizer:
        # np.random.seed(1)

        # generate random x,y coordinates (columns, rows):
        columns = width * np.random.random((1, n))
        rows = height * np.random.random((1, n))

        # put these coordinates into the sea as 1s:
        zeros[rows.astype(np.int), columns.astype(np.int)] = 1

        # dilate them:
        # filter_sigma = w / (4. * n)
        filter_sigma = 5
        land = filters.gaussian(zeros, sigma=filter_sigma)

        # return boolean map: True/False
        return land > 0.7 * land.mean()

    @staticmethod
    def generate_mountains(height, width):
        # TODO: repetitive functions. can be generalized.
        # generate mountains map.
        sea = np.zeros((height, width))

        # number of seeds for mountains
        n = 25

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
        filter_sigma = 2
        mountains = filters.gaussian(sea, sigma=filter_sigma)

        # make it TrueFalse map:
        return mountains > 0.7 * mountains.mean()


    @staticmethod
    def generate_minimap(tile_dict, rows, cols):
        rgb = np.zeros((cols, rows, 3), dtype=np.uint8)
        rgb[:, :, :] = [50, 80, 255]  # all set to blue
        # populate colors:
        for k, tile in tile_dict.items():
            if tile.type == 'land':
                color = [0, 255, 0]
                rgb[tile.c, tile.r, :] = color
            elif tile.type == 'mountain':
                color = [120, 120, 120]
                rgb[tile.c, tile.r, :] = color
            elif tile.type == 'sand':
                color = [240, 240, 0]
                rgb[tile.c, tile.r, :] = color
        mini_map = pg.surfarray.make_surface(rgb)
        return mini_map

    @staticmethod
    def generate_from_txt(game, sprites_group):
        file_path = os.path.join(FOLDER_RESOURCES, 'map_1.txt')
        data = []
        with open(file_path, 'rt') as f:
            for line in f:
                data.append(line)
        rows = len(data)
        cols = len(data[0])
        number_map = np.zeros((rows, cols), dtype=np.uint8)

        for row, tiles in enumerate(data):
            for col, el in enumerate(tiles):
                number_map[row, col] = int(el)

        tile_dict = MapGenerator.generate_tiles(game, sprites_group, number_map)
        return tile_dict

        #         # generate a tile:
        #         tile_dict[str(row) + '.' + str(col)] = Tile(game, row, col, tile_type)
        #
        # MapInfo = namedtuple('MapInfo',
        #                      ['tile_dict', 'width_in_tile_numbers', 'height_in_tile_numbers',
        #                      'height_in_pix', 'width_in_pix'])
        #
        # map_info = MapInfo(tile_dict=tile_dict,
        #                    width_in_tile_numbers=width_in_tiles_numbers,
        #                    height_in_tile_numbers=height_in_tiles_numbers,
        #                    height_in_pix=height_in_pix,
        #                    width_in_pix=width_in_pix)
        # return map_info
