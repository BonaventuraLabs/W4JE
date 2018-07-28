import numpy as np
from src.player.Units import Ship, Castle
from src.utilities.settings import *

class Player:
    def __init__(self, game, name, color):
        self.game = game
        self.color = color#np.random.randint(0, 255, size=(1, 3))
        self.name = name
        self.turn_finished = False
        row = np.random.randint(0, MAP_TILE_H)
        col = np.random.randint(0, MAP_TILE_W)
        self.ship = Ship(game, self, row, col)
        self.castle = Castle(game, self)
        self.is_done = True  # not his turn at creation
        self.is_current = False
        self.moved = False

    def set_current(self):
        self.is_done = False
        self.is_current = True
        self.ship.recalc_center()
        self.game.camera.update(self.ship.rect.x, self.ship.rect.y)

    def unset_current(self):
        self.is_done = True
        self.is_current = False