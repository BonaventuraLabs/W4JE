import pygame as pg
import numpy as np


class Player:
    def __str__(self, game, name, color):
        self.game = game
        self.color = color#np.random.randint(0, 255, size=(1, 3))
        self.name = name
        self.turn_finished = False
        self.ship = ship
