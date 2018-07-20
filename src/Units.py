import pygame as pg
from src.settings import *
import numpy as np
from collections import namedtuple
vec = pg.math.Vector2

class Ship(pg.sprite.Sprite):
    def __init__(self, game, row, col, name, color):
        self.name = name
        self.color = color
        self.groups = game.unit_sprites, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILEWIDTH/2, TILEWIDTH/2))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.r = row
        self.c = col
        self.xy = None
        self.recalc_center()
        self.rect.center = self.xy
        self.is_done = True # not his turn at creation
        self.is_current = False
        # self.v = vec(0, 0)

    def set_current(self):
        self.is_done = False
        self.is_current = True
        self.game.camera.update(self)

    def unset_current(self):
        self.is_done = True
        self.is_current = False

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

    def check_key_input(self):
        #TODO: wind effect.
        #w = self.game.wind.current_strength
        #TODO: animation of moving? Otherwise the update is too abrupt.
        keys = pg.key.get_pressed()
        moved = False
        if keys[pg.K_KP1]:
            self.move_ld()
            moved = True
        if keys[pg.K_KP3]:
            self.move_rd()
            moved = True
        if keys[pg.K_KP4]:
            self.move_l()
            moved = True
        if keys[pg.K_KP6]:
            self.move_r()
            moved = True
        if keys[pg.K_KP7]:
            self.move_lu()
            moved = True
        if keys[pg.K_KP9]:
            self.move_ru()
            moved = True
        if moved:
            self.unset_current()

    def draw(self):
        if self.is_current:
            # draw square surface:
            D = 60 # TILEWIDTH*0.75
            sel_surf = pg.Surface((D, D), pg.SRCALPHA, 32).convert_alpha()
            # sel_surf.fill(LIGHTGREY)
            # draw circle on this surface:
            circ_center = (int(D / 2), int(D / 2))
            pg.draw.circle(sel_surf, WHITE,  circ_center, int(TILEWIDTH*0.75), 3)
            pg.draw.circle(sel_surf, WHITE,  circ_center, int(TILEWIDTH*0.95), 3)

            # set proper center coordinate for this surface:
            rect = sel_surf.get_rect()
            rect.center = self.xy

            # Now: camera.apply(object)  - object must have this attribute: object.rect
            # For that I make a namedtuple: CustomRect.rect
            # where i will store rect. Cool, eh? - the power of python :)
            CustomRect = namedtuple('CustomRect', ['rect'])
            cust_rect = CustomRect(rect)

            self.game.screen.blit(sel_surf, self.game.camera.apply(cust_rect))
        self.game.screen.blit(self.image, self.game.camera.apply(self))

    def update(self, *args):
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
