import pygame as pg
from src.Settings import *
import os
import numpy as np
from skimage import filters
from collections import namedtuple
from src.Settings import *


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

        #surf = pg.surfarray.make_surface(Z)

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


class Map:
    def __init__(self, game):
        self.game = game
        #map_info = MapGenerator.generate_from_txt(game)
        map_info = MapGenerator.generate_from_numpy(game, 100, 100)
        self.tiles_dict = map_info.tile_dict

        # TODO: minimap = pg.Surface()

        self.tilewidth = map_info.width_in_tile_numbers
        self.tileheight = map_info.height_in_tile_numbers
        self.height = map_info.height_in_pix
        self.width = map_info.width_in_pix

    def draw(self):
        pass

    def update(self):
        pass


class Tile(pg.sprite.Sprite):
    def __init__(self, game, row, col, tile_type):
        self.type = tile_type
        self.groups = game.sprites_map, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.type == 'sea':
            self.image = self.game.image_manager.sea
        elif self.type == 'land':
            self.image = self.game.image_manager.land
        elif self.type == 'mountain':
            self.image = self.game.image_manager.land
            self.image.blit(self.game.image_manager.mountain, (0, 0))

        self.rect = self.image.get_rect()

        self.c = col
        self.r = row
        self.rc_str = str(self.r) + ', ' + str(self.c)

        # recalculate x, y
        self.center = Tile.recalculate_xy(self.r, self.c)
        self.rect.center = self.center

    @staticmethod
    def recalculate_xy(r, c):
        rx = TILER * np.cos(np.pi / 6)
        ry = TILER

        # real coordinates on map;
        # shift to right each 2nd row
        if r % 2 == 0:
            x = c * 2 * rx
            y = r * 1.5 * ry
        else:
            x = c * 2 * rx + rx  # here we shift to right.
            y = r * 1.5 * ry
        return x, y


class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.speed = CAMERA_SPEED

    # def apply(self, target):
    #     return target.rect.move(self.camera.topleft)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, x, y):
        # def update(self, target):
        #     x = -target.rect.x + int(WIDTH/2)
        #     y = -target.rect.y + int(HEIGHT/2)
        #     self.camera = pg.Rect(x, y, self.width, self.height)

        # same as old, but directly with x and y; this is more flexible than "target.rect.x"
        x_shifted = - x + int(WIDTH / 2)
        y_shifted = - y + int(HEIGHT / 2)
        self.rect = pg.Rect(x_shifted, y_shifted, self.width, self.height)

    def move_left(self):
        self.rect.x += self.speed

    def move_right(self):
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y += self.speed

    def move_down(self):
        self.rect.y -= self.speed


class Wind:
    def __init__(self, game):
        self.game = game
        self.directions = {'N':0, 'NW':45, 'W':90, 'SW': 135, 'S':180, 'SE':225, 'E':270, 'NE':315}
        self.current_direction = 'N'
        self.current_angle = 0
        self.strengths = [0, 1, 2, 3, 4]
        self.current_strength = 3
        # 0 - shtil, 4 - storm.

    def update(self, *args):
        pass#self.get_new_direction()

    def get_new_direction(self):

        self.current_direction = np.random.choice(list(self.directions.keys()))
        self.current_angle = self.directions[self.current_direction]
        self.current_strength = np.random.choice(self.strengths)
        # print(self.current_direction)


class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = np.random.choice(self.game.image_manager.cloud_list)
        self.rect = self.image.get_rect()
        self.rect.center = (np.random.randint(0, self.game.map.width),
                            np.random.randint(0, self.game.map.height))
        self.frame_skipper = 0
        self.frame_skipper_max = 10

    def update(self, *args):
        # make it slower!!!.
        if self.frame_skipper < self.frame_skipper_max:
            self.frame_skipper += 1
            return
        else:
            self.frame_skipper = 0

        angle = self.game.wind.current_angle
        self.rect.x += self.game.wind.current_strength * np.cos(np.deg2rad(90 + angle))
        self.rect.y -= self.game.wind.current_strength * np.sin(np.deg2rad(90 + angle))

        if self.rect.left > self.game.map.width:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.game.map.width
        if self.rect.top > self.game.map.height:
            self.rect.bottom = 0
        if self.rect.bottom > self.game.map.height:
            self.rect.top = self.game.map.height

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))



class Seagull(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.image_manager.seagull
        self.rect = self.image.get_rect()

        self.frame_skipper = 0
        self.frame_skipper_max = 2

        self.orbit_r = np.random.randint(0, 200)
        self.orbit_c = (np.random.randint(0, self.game.map.width),
                        np.random.randint(0, self.game.map.height))
        self.initial_angle = np.random.randint(0, 360)

        # self.rect.center
        self.recalculate_position()

    def recalculate_position(self):
        initial_pos = (self.orbit_c[0] + self.orbit_r * np.cos(np.deg2rad(self.initial_angle)),
                       self.orbit_c[1] + self.orbit_r * np.sin(np.deg2rad(self.initial_angle)))
        self.rect.center = initial_pos
        # return initial_pos

    def update(self, *args):
        # make it slower!!!.
        if self.frame_skipper < self.frame_skipper_max:
            self.frame_skipper += 1
            return
        else:
            self.frame_skipper = 0

        self.initial_angle += 1
        self.recalculate_position()

        # angle = self.game.wind.current_angle

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))

