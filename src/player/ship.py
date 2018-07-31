import numpy as np
from src.utilities.settings import *
from src.player.aura import Aura
import pygame as pg


class Ship(pg.sprite.Sprite):
    def __init__(self, game, player, row, col):
        self.game = game
        self.player = player
        self.groups = self.game.sprites_unit, self.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
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
        self.moving_anim_on = False
        self.moves_per_turn = 2  # equivalent of speed
        self.moves_left = self.moves_per_turn

    def recalc_center(self):
        self.r_prev = self.r
        self.c_prev = self.c
        self.xy_prev = self.xy
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy
        self.aura.set_center(self.xy)


    def on_click(self):
        print('Click : ' + self.player.name + ' ship')


    # TODO: wind effect.
    def on_moved(self):
        self.moves_left -= 1
        self.recalc_center()
        self.moving_anim_on = True
        # set back for animation
        self.rect.center = self.xy_prev  # self.xy
        self.aura.set_center(self.rect.center)
        #print(self.xy_prev)
        #print(self.xy)

    def draw(self):
        if self.player.is_current:
            self.game.screen.blit(self.aura.image, self.game.camera.apply(self.aura))
        self.game.screen.blit(self.image, self.game.camera.apply(self))
        label, label_rect = self.get_name_label()
        self.game.screen.blit(label, self.game.camera.apply(label_rect))

    def get_name_label(self):
        text = self.player.name
        label = self.game.font.render(text, True, WHITE)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        label_rect.bottom = self.rect.bottom
        return label, label_rect

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
                # self.player.unset_current()

        # shuffle aura
        if self.player.is_current:
            self.aura.update()

    def check_what_in_target_tile(self):
        print('Check what in target tile')

    def move(self, event_key):
        if self.moves_left <= 0:
            print(self.player.name + ': ship is out of moves.')
            return

        if event_key == pg.K_KP1:
            self.move_ld()
        elif event_key == pg.K_KP3:
            self.move_rd()
        elif event_key == pg.K_KP4:
            self.move_l()
        elif event_key == pg.K_KP6:
            self.move_r()
        elif event_key == pg.K_KP7:
            self.move_lu()
        elif event_key == pg.K_KP9:
            self.move_ru()

    def move_l(self):
        self.check_what_in_target_tile()
        self.c -= 1
        self.on_moved()

    def move_r(self):
        self.check_what_in_target_tile()
        self.c += 1
        self.on_moved()

    def move_ru(self):
        self.check_what_in_target_tile()
        if self.r % 2 == 0:
            self.r -= 1
            self.c += 0
        else:
            self.r -= 1
            self.c += 1
        self.on_moved()

    def move_lu(self):
        self.check_what_in_target_tile()
        if self.r % 2 == 0:
            self.r -= 1
            self.c -= 1
        else:
            self.r -= 1
            self.c -= 0
        self.on_moved()

    def move_rd(self):
        self.check_what_in_target_tile()
        if self.r % 2 == 0:
            self.r += 1
            self.c += 0
        else:
            self.r += 1
            self.c += 1
        self.on_moved()

    def move_ld(self):
        self.check_what_in_target_tile()
        if self.r % 2 == 0:
            self.r += 1
            self.c -= 1
        else:
            self.r += 1
            self.c += 0
        self.on_moved()
