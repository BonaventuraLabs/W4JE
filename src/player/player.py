import numpy as np
from src.player.ship import Ship
from src.player.castle import Castle
from src.utilities.settings import *
import pygame as pg


class Player:

   # original # keys_ship_move = [pg.K_KP1, pg.K_KP3, pg.K_KP4, pg.K_KP6, pg.K_KP7, pg.K_KP9]


    def __init__(self, game, name, color):
        self.game = game
        self.color = color
        self.name = name

        # position at generation:
        # shuffle available tiles:
        np.random.shuffle(self.game.map.spawn_tiles_list)
        row, col = self.game.map.spawn_tiles_list.pop()

        # random (even on land):
        # row = np.random.randint(0, MAP_TILE_H)
        # col = np.random.randint(0, MAP_TILE_W)

        self.castle = Castle(game, self, row, col)
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



