import pygame as pg
from src.Settings import *
import numpy as np
from collections import namedtuple
vec = pg.math.Vector2


class Aura(pg.sprite.Sprite):
    def __init__(self, owner):
        self.groups = owner.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.owner = owner
        self.image = self.generate_image()
        # proper position:
        self.rect = self.image.get_rect()

        self.image_fixed = self.image.copy()
        self.rect_fixed = self.rect.copy()

        self.phase_speed = 0.001
        self.phase_min = 0.75
        self.phase_max = 1
        self.phase = self.phase_max
        self.phase_change = -self.phase_speed

    def generate_image(self):
        # square surface, 2*tile:
        w = 2 * TILEWIDTH
        sel_surf = pg.Surface((w, w), pg.SRCALPHA, 32).convert_alpha()

        # draw circle in the center of this surface:
        center = (int(TILEWIDTH), int(TILEWIDTH))
        r1 = int(TILEWIDTH * 0.75)
        r2 = int(TILEWIDTH * 0.95)
        thickness = 3
        pg.draw.circle(sel_surf, self.owner.color, center, r1, 0)
        pg.draw.circle(sel_surf, self.owner.color, center, r2, thickness)
        return sel_surf

    def set_center(self, xy):
        self.rect.center = xy

    def update(self):
        # oscillating (triangle oscillator) of the phase between phase_min and max:
        if self.phase >= self.phase_max:
            self.phase_change = -self.phase_speed
        if self.phase <= self.phase_min:
            self.phase_change = +self.phase_speed
        self.phase += self.phase_change
        new_w = int(self.rect_fixed.w * self.phase)
        new_h = int(self.rect_fixed.h * self.phase)
        self.image = pg.transform.scale(self.image_fixed, (new_w, new_h))
        self.rect = self.image.get_rect()
        self.rect.center = self.owner.xy


class Ship(pg.sprite.Sprite):
    def __init__(self, game, row, col, name, color):
        self.groups = game.sprites_unit, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.color = color
        self.game = game
        self.image = self.game.image_manager.ship
        self.aura = Aura(self)
        self.rect = self.image.get_rect()
        self.r = row
        self.c = col
        self.xy = None
        self.recalc_center()
        self.r_prev = row
        self.c_prev = col
        self.xy_prev = self.xy[:]
        self.rect.center = self.xy
        self.is_done = True  # not his turn at creation
        self.is_current = False
        self.moved = False
        self.moving_anim_on = False

    def set_current(self):
        self.is_done = False
        self.is_current = True
        self.recalc_center()
        self.game.camera.update(self.rect.x, self.rect.y)

    def unset_current(self):
        self.is_done = True
        self.is_current = False

    def recalc_center(self):
        self.r_prev = self.r
        self.c_prev = self.c
        self.xy_prev = self.xy

        # bounding box of a tile:
        rx = TILER * np.cos(np.pi / 6)
        ry = TILER

        # real coordinates on map;
        # shift to right each 2nd row
        if self.r % 2 == 0:
            x = self.c * 2 * rx
            y = self.r * 1.5 * ry
        else:
            x = self.c * 2 * rx + rx  # here we shift to right.
            y = self.r * 1.5 * ry
        self.xy = [x, y]
        self.rect.center = self.xy
        self.aura.set_center(self.xy)

    # TODO: wind effect.
    def on_moved(self):
        self.recalc_center()
        self.moving_anim_on = True
        # set back for animation
        self.rect.center = self.xy_prev  # self.xy
        self.aura.set_center(self.rect.center)
        #print(self.xy_prev)
        #print(self.xy)


    def draw(self):
        if self.is_current:
            self.game.screen.blit(self.aura.image, self.game.camera.apply(self.aura))
        self.game.screen.blit(self.image, self.game.camera.apply(self))
        self.game.screen.blit(self.get_label(), self.game.camera.apply(self))

    def get_label(self):
        text = self.name
        label = self.game.font.render(text, True, BLACK)
        label.get_rect().center = self.rect.center
        label.get_rect().bottom = self.rect.bottom
        return label

    def update(self, *args):

        if self.moving_anim_on:

            # print('------')
            # print(self.xy_prev)
            # print(self.xy)

            # check in which direction should move:
            dx = self.xy[0] - self.rect.center[0]
            dy = self.xy[1] - self.rect.center[1]

            # print(dx)

            if dx > 0:
                self.rect.center = (self.rect.center[0]+1, self.rect.center[1])  # stupid, because tuple cannot be += 1
            if dx < 0:
                self.rect.center = (self.rect.center[0] - 1, self.rect.center[1])
            if dy > 0:
                self.rect.center = (self.rect.center[0], self.rect.center[1] + 1)
            if dy < 0:
                self.rect.center = (self.rect.center[0], self.rect.center[1] - 1)

            self.aura.set_center(self.rect.center)

            # check if done
            if abs(dx) < 1 and abs(dy) < 1:
                self.moving_anim_on = False
                self.rect.center = self.xy
                self.aura.set_center(self.xy)
                self.unset_current()

        # shuffle aura
        if self.is_current:
            self.aura.update()


    def move_l(self):
        self.c -= 1
        self.on_moved()

    def move_r(self):
        self.c += 1
        self.on_moved()

    def move_ru(self):
        if self.r % 2 == 0:
            self.r -= 1
            self.c += 0
        else:
            self.r -= 1
            self.c += 1
        self.on_moved()

    def move_lu(self):
        if self.r % 2 == 0:
            self.r -= 1
            self.c -= 1
        else:
            self.r -= 1
            self.c -= 0
        self.on_moved()

    def move_rd(self):
        if self.r % 2 == 0:
            self.r += 1
            self.c += 0
        else:
            self.r += 1
            self.c += 1
        self.on_moved()

    def move_ld(self):
        if self.r % 2 == 0:
            self.r += 1
            self.c -= 1
        else:
            self.r += 1
            self.c += 0
        self.on_moved()
