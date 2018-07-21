import pygame as pg
from src.Settings import *


class ImageManager:
    def __init__(self, game):
        self.game = game

        sea = ImageManager.load(TILE_SEA_IMAGE)
        self.sea = pg.transform.scale(sea, (TILEWIDTH, TILEHEIGHT))

        land = ImageManager.load(TILE_LAND_IMAGE)
        self.land = pg.transform.scale(land, (TILEWIDTH, TILEHEIGHT))

        mountain = ImageManager.load(TILE_MOUNTAIN_IMAGE)
        self.mountain = pg.transform.scale(mountain, (TILEWIDTH, TILEHEIGHT))

        ship = ImageManager.load(SHIP)
        self.ship = pg.transform.scale(ship, (TILEWIDTH, TILEHEIGHT))

        wind_arrow = ImageManager.load(WIND_ARROW)
        self.wind_arrow = pg.transform.scale(wind_arrow, (30, 100))

        compass = ImageManager.load(HUD_COMPASS)
        self.hud_compass = pg.transform.scale(compass, (120, 120))

        scroll = ImageManager.load(HUD_SCROLL)
        self.hud_scroll = pg.transform.scale(scroll, (200, HEIGHT))

    @staticmethod
    def load(name):
        image = pg.image.load(os.path.join(FOLDER_RESOURCES, name)).convert_alpha()
        return image

