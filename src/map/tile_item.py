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


class Animal:

    name_list = ['Lisa', 'Mishka', 'Sobachka']

    def __init__(self, tile):
        self.game = tile.game
        self.tile = tile
        self.image = np.random.choice(self.game.image_manager.animals_list)
        self.name = np.random.choice(Animal.name_list)
        self.rect = self.image.get_rect()

