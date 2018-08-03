import numpy as np
from src.player.ship import Ship
from src.player.castle import Castle
from src.utilities.settings import *
import pygame as pg


class Player:

    keys_ship_move = [pg.K_KP1, pg.K_KP3, pg.K_KP4, pg.K_KP6, pg.K_KP7, pg.K_KP9]
    keys_end_turn = [pg.K_KP_ENTER]
    keys_all = keys_ship_move + keys_end_turn

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
        self.ship = Ship(game, self, row, col)

        # turn parameters
        # self.turn_finished = False
        # not his turn at creation:
        self.is_current = False
        self.is_done = True

    def handle_keys(self, event):
        if event.key in Player.keys_ship_move:
            self.ship.handle_keys(event)

        if event.key == pg.K_KP_ENTER:
            self.game.player_turn_manager.end_turn()