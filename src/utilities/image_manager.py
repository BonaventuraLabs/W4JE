import pygame as pg
from src.utilities.settings import *


class ImageManager:
    def __init__(self, game):
        self.game = game

        sea = ImageManager.load(TILE_SEA_IMAGE)
        self.sea = pg.transform.scale(sea, (TILEWIDTH, TILEHEIGHT))

        sand = ImageManager.load(TILE_SAND_IMAGE)
        self.sand = pg.transform.scale(sand, (TILEWIDTH, TILEHEIGHT))

        land = ImageManager.load(TILE_LAND_IMAGE)
        self.land = pg.transform.scale(land, (TILEWIDTH, TILEHEIGHT))

        mountain = ImageManager.load(TILE_MOUNTAIN_IMAGE)
        # put mountains onto the land:
        land_base = land#.copy()
        land_base.blit(mountain, (0, 0))
        self.mountain = pg.transform.scale(land_base, (TILEWIDTH, TILEHEIGHT))

        ship = ImageManager.load(SHIP)
        self.ship = pg.transform.scale(ship, (TILEWIDTH, TILEHEIGHT))

        wind_arrow = ImageManager.load(WIND_ARROW)
        self.wind_arrow = pg.transform.scale(wind_arrow, (30, 100))

        compass = ImageManager.load(HUD_COMPASS)
        self.hud_compass = pg.transform.scale(compass, (120, 120))

        scroll = ImageManager.load(HUD_SCROLL)
        self.hud_scroll = pg.transform.scale(scroll, (200, HEIGHT))

        seagull = ImageManager.load(SEAGULL)
        self.seagull = pg.transform.scale(seagull, (40, 20))

        castle = ImageManager.load(CASTLE)
        self.castle = pg.transform.scale(castle, (3*TILEWIDTH, 3*TILEHEIGHT))

        self.cloud_list = ImageManager.load_cloud_list()

    @staticmethod
    def load(name):
        image = pg.image.load(os.path.join(FOLDER_RESOURCES, name)).convert_alpha()
        return image

    @staticmethod
    def load_cloud_list():
        cloud_list = []
        for i in range(1, 7):
            img_name = CLOUDS_1_6[0] + str(i) + CLOUDS_1_6[1]
            img = ImageManager.load(img_name)
            # img.set_alpha(10)  # does not work if an image ha its own per-poxel transparency
            # resize?
            img = pg.transform.scale(img, (300, 100))
            cloud_list.append(img)
        return cloud_list
