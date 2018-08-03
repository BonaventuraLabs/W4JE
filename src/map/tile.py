import pygame as pg
import numpy as np
from src.map.tile_item import TileItem


class Tile(pg.sprite.Sprite):
    def __init__(self, game, sprites_group, row, col, tile_type):
        self.game = game
        self.groups = sprites_group # self.game.sprites_map, #self.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)

        self.c = col
        self.r = row
        self.rc_str = str(self.r) + ', ' + str(self.c)

        self.type = tile_type
        if self.type == 'sea':
            self.image_base = self.game.image_manager.sea
            self.image = self.game.image_manager.sea
        elif self.type == 'sand':
            self.image_base = self.game.image_manager.sand
            self.image = self.game.image_manager.sand
        elif self.type == 'land':
            self.image_base = self.game.image_manager.land
            self.image = self.game.image_manager.land
        elif self.type == 'mountain':
            self.image_base = self.game.image_manager.mountain
            self.image = self.game.image_manager.mountain

        self.rect = self.image.get_rect()
        self.center = None
        # real xy coordinates are recalculated in Map, afte rthe tile dict has been generated.
        # I had to do it thre, because I cannot import Map to use its method rc_to_xy.
        # Import is forbidden, because it loops the imports: Map -> Generator -> Tile -> Map.

        self.item = None
        self.add_item()

        # TODO: fog of war.
        self.discovered_by = []

    def add_item(self):
        chances = (1, 200) # 1 out of N
        if np.random.randint(0, chances[1], 1) < chances[0]:
            self.item = TileItem(self)
            img = self.image_base.copy()
            img.blit(self.item.image, (0, 0))
            self.image = img#.blit(self.item.image, (0, 0))

    def remove_item(self):
        self.item = None
        self.image = self.image_base

    def on_click(self):
        print('Click : ' + self.__str__())

    def __str__(self):
        return 'Tile: ' + self.type + '; r.c = ' + self.rc_str

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))