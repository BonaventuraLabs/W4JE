import pygame as pg
from src.settings import *

class ImageLoader:
    def __init__(self, game):
        self.game = game
        self.sea_1 = ImageLoader.load(TILE_SEA_IMAGE)
        self.land_1 = ImageLoader.load(TILE_LAND_IMAGE)
        self.wind_arrow_1 = ImageLoader.load(WIND_ARROW)

    @staticmethod
    def load(name):
        image = pg.image.load(os.path.join(FOLDER_RESOURCES, name)).convert_alpha()
        return image


class Hud(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.top_layer_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        self.image.fill((250, 250, 180))
        self.rect = self.image.get_rect()

