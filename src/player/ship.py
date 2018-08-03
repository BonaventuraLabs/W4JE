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

    def recalc_center(self):
        self.r_prev = self.r
        self.c_prev = self.c
        self.xy_prev = self.xy
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy
        self.aura.set_center(self.xy)

    # TODO: wind effect.
    def make_move(self):
        self.moves_left -= 1
        self.recalc_center()
        self.moving_anim_on = True
        # set back for animation
        self.rect.center = self.xy_prev  # self.xy
        self.aura.set_center(self.rect.center)
        #print(self.xy_prev)
        #print(self.xy)

    def handle_keys(self, event):
        # check if there are moves left:
        if self.moves_left <= 0:
            print(self.player.name + ': ship is out of moves.')
            return

        # see where the keys suggest to move to:
        r, c = self.get_target_rc(event)
        target_tile = self.game.map.get_tile_by_rc(r, c)
        print('targeted tile: ' + target_tile.__str__())

        # if water - can make move. Otherwise, not.
        if target_tile.type == 'sea': # or river???
            self.r = r
            self.c = c
            self.make_move()
        else:
            print('Cant move')

    def get_target_rc(self, event):
        r = None
        c = None
        if event.key == pg.K_KP1:
            if self.r % 2 == 0:
                r = self.r + 1
                c = self.c - 1
            else:
                r = self.r + 1
                c = self.c
        elif event.key == pg.K_KP3:
            if self.r % 2 == 0:
                r = self.r + 1
                c = self.c
            else:
                r = self.r + 1
                c = self.c + 1
        elif event.key == pg.K_KP4:
            r = self.r
            c = self.c - 1
        elif event.key == pg.K_KP6:
            r = self.r
            c = self.c + 1
        elif event.key == pg.K_KP7:
            if self.r % 2 == 0:
                r = self.r - 1
                c = self.c - 1
            else:
                r = self.r - 1
                c = self.c
        elif event.key == pg.K_KP9:
            if self.r % 2 == 0:
                r = self.r - 1
                c = self.c
            else:
                r = self.r - 1
                c = self.c + 1
        return r, c

    def on_click(self):
        print('Click : ' + self.player.name + ' ship')

