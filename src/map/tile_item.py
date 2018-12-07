import pygame as pg
import numpy as np


# class Animal:
#     def __init__(self, tile):
#         self.game = tile.game
#         self.tile = tile
#         self.image = np.random.choice(self.game.image_manager.fish_list)
#         self.name = np.random.choice(Fish.name_list)
#         self.rect = self.image.get_rect()
#
#     def move(self):
#         pass


class Fish:

    name_list = ['Ershik', 'RibaCop 3', 'Akula', 'Nemo', 'Neptun']

    def __init__(self, tile):
        self.game = tile.game
        self.tile = tile
        self.image = np.random.choice(self.game.image_manager.fish_list)
        self.name = np.random.choice(Fish.name_list)
        self.rect = self.image.get_rect()


class Landscape:

    def __init__(self, tile):
        self.game = tile.game
        self.name = 'Landscape'
        self.tile = tile
        self.image = np.random.choice(self.game.image_manager.landscape_list)
        self.rect = self.image.get_rect()