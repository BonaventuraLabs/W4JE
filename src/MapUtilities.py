import pygame as pg
from src.settings import *
from src.Units import Ship
import os
import numpy as np

vec = pg.math.Vector2


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
                elif el == 'P':
                    self.game.ship = Ship(self.game, row, col)
                else:
                    tile_type = 'sea'

                tile_dict[str(row) + '.' + str(col)] = Tile(self.game, row, col, tile_type)
        return tile_dict


class Tile(pg.sprite.Sprite):
    def __init__(self, game, row, col, tile_type):
        self.type = tile_type
        self.groups = game.map_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.type == 'sea':
            self.image = self.game.images.sea_1
        elif self.type == 'land':
            self.image = self.game.images.land_1
        else:
            self.image = self.game.images.sea_1

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

    def apply(self, target):
        return target.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        self.camera = pg.Rect(x, y, self.width, self.height)

