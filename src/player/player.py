import numpy as np
from src.player.ship import Ship
from src.player.castle import Castle
from src.player.village import Village
from src.utilities.settings import *
import pygame as pg


class Player:

   # original # keys_ship_move = [pg.K_KP1, pg.K_KP3, pg.K_KP4, pg.K_KP6, pg.K_KP7, pg.K_KP9]


    def __init__(self, game, name, color, rw, cl, nation):
        self.game = game
        self.color = color
        self.name = name
        self.nation = nation
        # UNDELETE if random spawn is needed
        # position at generation:
        # shuffle available tiles:
        #np.random.shuffle(self.game.map.spawn_tiles_list)
        #row, col = self.game.map.spawn_tiles_list.pop()

        row, col = [rw, cl]

        #self.row = rw
        #self.col = cl

        # random (even on land):
        # row = np.random.randint(0, MAP_TILE_H)
        # col = np.random.randint(0, MAP_TILE_W)

        self.castle = Castle(game, self, row, col)
        if row == 4:
            vr1 = 45
            vc1 = 10
            vr2 = 46
            vc2 = 32
        elif row == 25:
            if col == 4:
                vr1 = 14
                vc1 = 42
                vr2 = 36
                vc2 = 42
            elif col == 45:
                vr1 = 14
                vc1 = 5
                vr2 = 38
                vc2 = 7
        else:
            vr1 = 5
            vc1 = 10
            vr2 = 5
            vc2 = 36

        self.villages = []
        self.villages.append(Village(game, self, vr1, vc1))
        self.villages.append(Village(game, self, vr2, vc2))
        self.ships = []
        self.ships.append(Ship(game, self, row, col, 'Sloop'))
        self.ships.append(Ship(game, self, row, col, 'Sloop'))
        self.ships.append(Ship(game, self, row, col, 'Brigantine'))


        # turn parameters
        # self.turn_finished = False
        # not his turn at creation:
        self.is_current = False
        self.is_done = True

    def get_ship_by_xy(self, x, y):
        for s in self.ships:
            if s.r == x:
                if s.c == y:
                    return s



