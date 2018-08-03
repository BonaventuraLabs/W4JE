import pygame as pg
import numpy as np

class TileItem:

    name_list = ['bobik', 'ribka 2', 'akula', 'sharik', 'krok']
    item_count = 0

    def __init__(self, tile):
        self.game = tile.game
        self.tile = tile
        self.image = np.random.choice(self.game.image_manager.fish_list)
        self.name = np.random.choice(TileItem.name_list)
        self.rect = self.image.get_rect()
        # TileItem.item_count += 1
        # print(TileItem.item_count)



