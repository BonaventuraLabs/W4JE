import pygame as pg
from src.utilities.settings import *
import numpy as np


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
            self.image = self.game.image_manager.mountain

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

    def __str__(self):
        return 'Tile: ' + self.type + '; r.c = ' + self.rc_str

