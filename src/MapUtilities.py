import pygame as pg
from src.settings import *
import os
import numpy as np
from skimage import filters


class MapGenerator:

    @staticmethod
    def generate_pixel_map(h, w):
        land = MapGenerator.generate_land(h, w)
        mountains = MapGenerator.generate_land(h, w)

        # add mountains ONLY to the land:
        full_map = land + land * mountains
        return full_map

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
    def show(pixel_map):
        pass
        # fig, ax = plt.subplots(1)
        # ax.imshow(pixel_map)
        # plt.show()


class Map:
    def __init__(self, game):
        self.game = game
        file_path = os.path.join(FOLDER_RESOURCES, 'map_1.txt')
        self.data = []
        with open(file_path, 'rt') as f:
            for line in f:
                self.data.append(line)
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)

        #TODO: wrong. height is not N*y, because the tiles are shifted
        self.height = self.tileheight * TILEHEIGHT
        self.width = self.tilewidth * TILEWIDTH
        self.tiles_dict = self.generate_tiles()

    def draw(self):
        pass

    def update(self):
        pass

    def generate_tiles(self):
        tile_dict = {}
        for row, tiles in enumerate(self.data):
            for col, el in enumerate(tiles):
                if el == '1':
                    tile_type = 'land'
                elif el == '.':
                    tile_type = 'sea'
                # elif el == 'P':
                #     self.game.ship = Ship(self.game, row, col)
                else:
                    tile_type = 'sea'

                tile_dict[str(row) + '.' + str(col)] = Tile(self.game, row, col, tile_type)
        return tile_dict


class Tile(pg.sprite.Sprite):
    def __init__(self, game, row, col, tile_type):
        self.type = tile_type
        self.groups = game.map_sprites, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.type == 'sea':
            self.image = self.game.images.sea
        elif self.type == 'land':
            self.image = self.game.images.land
        else:
            self.image = self.game.images.sea

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
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.speed = CAMERA_SPEED

    def apply(self, target):
        return target.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        self.camera = pg.Rect(x, y, self.width, self.height)

    def check_key_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.camera.x += self.speed
        if keys[pg.K_RIGHT]:
            self.camera.x -= self.speed
        if keys[pg.K_UP]:
            self.camera.y += self.speed
        if keys[pg.K_DOWN]:
            self.camera.y -= self.speed
        # self.camera = pg.Rect(x, y, self.width, self.height)


class Wind():
    def __init__(self, game):
        self.game = game
        self.directions = {'N':0, 'NW':45, 'W':90, 'SW': 135, 'S':180, 'SE':225, 'E':270, 'NE':315}
        self.current_direction = 'N'
        self.strengths = [0, 1, 2, 3, 4]
        self.current_strength = 0
        # 0 - shtil, 4 - storm.

    def update(self, *args):
        pass#self.get_new_direction()

    def get_new_direction(self):
        self.current_direction = np.random.choice(list(self.directions.keys()))
        self.current_strength = np.random.choice(self.strengths)
        # print(self.current_direction)


