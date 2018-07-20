import pygame as pg
from src.settings import *


class ImageLoader:
    def __init__(self, game):
        self.game = game
        self.sea = ImageLoader.load(TILE_SEA_IMAGE)
        self.land = ImageLoader.load(TILE_LAND_IMAGE)

        wind_arrow = ImageLoader.load(WIND_ARROW)
        self.wind_arrow = pg.transform.scale(wind_arrow, (100, 100))

        compass = ImageLoader.load(HUD_COMPASS)
        self.hud_compass = pg.transform.scale(compass, (200, 200))

        # WIDTH

        scroll = ImageLoader.load(HUD_SCROLL)
        self.hud_scroll = pg.transform.scale(scroll, (200, HEIGHT))


    @staticmethod
    def load(name):
        image = pg.image.load(os.path.join(FOLDER_RESOURCES, name)).convert_alpha()
        return image


class Hud(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.top_layer_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        # self.image.fill((250, 250, 180))
        self.image = self.game.images.hud_scroll
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


