import pygame as pg
from src.Settings import *

'''Resources'''
FOLDER_RESOURCES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
TILE_SEA_IMAGE = 'tile_sea_1.png'
TILE_LAND_IMAGE = 'tile_land_1.png'
TILE_MOUNTAIN_IMAGE = 'tile_mountain_1.png'
WIND_ARROW = 'wind_arrow_2.png'
HUD_SCROLL = 'hud_scroll_2.png'
HUD_COMPASS = 'hud_compass_1.png'
SHIP = 'ship_1.png'
SEAGULL = 'image_seagull_1.png'

CLOUDS_1_6 = ['image_cloud_', '.png']


class ImageManager:
    def __init__(self, game):
        self.game = game

        sea = ImageManager.load(TILE_SEA_IMAGE)
        self.sea = pg.transform.scale(sea, (TILEWIDTH, TILEHEIGHT))

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
