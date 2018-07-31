import numpy as np
from src.player.ship import Ship
from src.player.castle import Castle
from src.utilities.settings import *
import pygame as pg


class Player:

    keys_move = [pg.K_KP1, pg.K_KP3, pg.K_KP4, pg.K_KP6, pg.K_KP7, pg.K_KP9, pg.K_KP_ENTER]
    keys_camera = [pg.K_KP5, pg.K_KP0]
    keys_all = keys_move + keys_camera

    def __init__(self, game, name, color):
        self.game = game
        self.color = color
        self.name = name

        # position at generation:
        row = np.random.randint(0, MAP_TILE_H)
        col = np.random.randint(0, MAP_TILE_W)
        self.castle = Castle(game, self, row, col)
        self.ship = Ship(game, self, row, col)

        # turn parameters
        # self.turn_finished = False
        # not his turn at creation:
        self.is_current = False
        self.is_done = True

    def handle_keys(self, event):
        if event.key in Player.keys_move:
            self.ship.move(event.key)

        if event.key in Player.keys_camera:
            if event.key == pg.K_KP5:
                self.game.camera.update(self.game.player_turn_manager.current_player.ship.rect.center[0],
                                        self.game.player_turn_manager.current_player.ship.rect.center[1])
            if event.key == pg.K_KP0:
                self.game.camera.update(self.game.player_turn_manager.current_player.castle.rect.center[0],
                                        self.game.player_turn_manager.current_player.castle.rect.center[1])
        if event.key == pg.K_KP_ENTER:
            self.game.player_turn_manager.end_turn()