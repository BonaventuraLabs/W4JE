import pygame as pg
from src.settings import *
import numpy as np

vec = pg.math.Vector2

class Ship(pg.sprite.Sprite):
    def __init__(self, game, row, col):
        self.groups = game.unit_sprites, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILEWIDTH/2, TILEWIDTH/2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.r = row
        self.c = col
        self.xy = None
        self.recalc_center()
        self.rect.center = self.xy
        # self.v = vec(0, 0)

    def recalc_center(self):
        r = self.r
        c = self.c
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
        self.xy = x, y
        self.rect.center = self.xy

    def update(self, *args):
        self.move()

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_KP1]:
            self.move_ld()
        if keys[pg.K_KP3]:
            print(3)
            self.move_rd()
        if keys[pg.K_KP4]:
            self.move_l()
        if keys[pg.K_KP6]:
            self.move_r()
        if keys[pg.K_KP7]:
            self.move_lu()
        if keys[pg.K_KP9]:
            self.move_ru()
        self.recalc_center()

    def move_l(self):
        self.c -= 1

    def move_r(self):
        self.c += 1

    def move_ru(self):
        if self.r % 2 == 0:
            self.r -= 1
            self.c += 0
        else:
            self.r -= 1
            self.c += 1

    def move_lu(self):
        if self.r % 2 == 0:
            self.r -= 1
            self.c -= 1
        else:
            self.r -= 1
            self.c -= 0

    def move_rd(self):
        if self.r % 2 == 0:
            self.r += 1
            self.c += 0
        else:
            self.r += 1
            self.c += 1

    def move_ld(self):
        if self.r % 2 == 0:
            self.r += 1
            self.c -= 1
        else:
            self.r += 1
            self.c += 0
