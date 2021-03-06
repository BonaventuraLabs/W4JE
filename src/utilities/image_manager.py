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

        sloophud = ImageManager.load(SLOOPHUD)
        self.sloophud = pg.transform.scale(sloophud, (180, 151))

        brigantinehud = ImageManager.load(BRIGANTINEHUD)
        self.brigantinehud = pg.transform.scale(brigantinehud, (180, 151))

        frigatehud = ImageManager.load(FRIGATEHUD)
        self.frigatehud = pg.transform.scale(frigatehud, (180, 151))

        ship = ImageManager.load(SHIP)
        self.ship = pg.transform.scale(ship, (TILEWIDTH, TILEHEIGHT))

        sloop = ImageManager.load(SLOOP)
        self.sloop = pg.transform.scale(sloop, (TILEWIDTH, TILEHEIGHT))

        brigantine = ImageManager.load(BRIGANTINE)
        self.brigantine = pg.transform.scale(brigantine, (TILEWIDTH, TILEHEIGHT))

        frigate = ImageManager.load(FRIGATE)
        self.frigate = pg.transform.scale(frigate, (TILEWIDTH, TILEHEIGHT))

        port = ImageManager.load(PORT)
        self.port = pg.transform.scale(port, (600, 500))

        starts = ImageManager.load(START)
        self.starts = pg.transform.scale(starts, (1400, 800))

        wind_arrow = ImageManager.load(WIND_ARROW)
        self.wind_arrow = pg.transform.scale(wind_arrow, (30, 100))

        compass = ImageManager.load(HUD_COMPASS)
        self.hud_compass = pg.transform.scale(compass, (120, 120))

        scroll = ImageManager.load(HUD_SCROLL)
        #self.hud_scroll = pg.transform.scale(scroll, (220, int(HEIGHT/20*19)))
        self.hud_scroll = pg.transform.scale(scroll, (220, HEIGHT))

        bottom_scroll = ImageManager.load(BOTTOM_SCROLL)
        self.bottom_scroll = pg.transform.scale(bottom_scroll, (800, 120))

        seagull = ImageManager.load(SEAGULL)
        self.seagull = pg.transform.scale(seagull, (40, 20))

        castle = ImageManager.load(CASTLE)
        self.castle = pg.transform.scale(castle, (2*TILEWIDTH, 2*TILEHEIGHT))

        village = ImageManager.load(VILLAGE)
        self.village = pg.transform.scale(village, (TILEWIDTH, TILEHEIGHT))

        ship_wreck = ImageManager.load(SHIP_WRECK)
        self.ship_wreck = pg.transform.scale(ship_wreck, (TILEWIDTH, TILEHEIGHT))

        #ship_capt = ImageManager.load(SHIP_CAPTURED)
        #self.ship_capt = pg.transform.scale(ship_capt, (4, 3))

        pirate_ship = ImageManager.load(PIRATE)
        self.pirate_ship = pg.transform.scale(pirate_ship, (TILEWIDTH, TILEHEIGHT))

        self.cloud_list = ImageManager.load_cloud_list()
        self.fish_list = ImageManager.load_fish_list()
        #self.animals_list = ImageManager.load_animals_list()
        self.landscape_list = ImageManager.load_landscape_list()

        #self.exp_list = ImageManager.load_explosion_list()
        self.exp_list = {'Sloop': [], 'Brigantine': [], 'Frigate': []}
        for i in range(9):
            filename = 'exp_{}.png'.format(i)
            img = pg.image.load(os.path.join(FOLDER_RESOURCES, filename)).convert_alpha()
            img.set_colorkey(BLACK)
            img_sl = pg.transform.scale(img, (TILEWIDTH, TILEHEIGHT))
            self.exp_list['Sloop'].append(img_sl)
            img_br = pg.transform.scale(img, (TILEWIDTH, TILEHEIGHT))
            self.exp_list['Brigantine'].append(img_br)
            img_br = pg.transform.scale(img, (TILEWIDTH, TILEHEIGHT))
            self.exp_list['Frigate'].append(img_br)

    #@staticmethod
    #def load_explosion_list():
    #    img_list = []
    #    for i in range(0, 9):
    #        img_name = EXPLOSION_1_9[0] + str(i) + EXPLOSION_1_9[1]
    #        img = ImageManager.load(img_name)
    #        img = pg.transform.scale(img, (TILEWIDTH, TILEWIDTH))
    #        img_list.append(img)
    #    return img_list

    @staticmethod
    def load(name):
        image = pg.image.load(os.path.join(FOLDER_RESOURCES, name)).convert_alpha()
        return image

    @staticmethod
    def load_cloud_list():
        img_list = []
        for i in range(1, 7):
            img_name = CLOUDS_1_6[0] + str(i) + CLOUDS_1_6[1]
            img = ImageManager.load(img_name)
            # img.set_alpha(10)  # does not work if an image ha its own per-poxel transparency
            # resize?
            img = pg.transform.scale(img, (300, 100))
            img_list.append(img)
        return img_list

    @staticmethod
    def load_fish_list():
        img_list = []
        for i in range(1, 3):
            img_name = FISH_1_2[0] + str(i) + FISH_1_2[1]
            img = ImageManager.load(img_name)
            # resize?
            img = pg.transform.scale(img, (TILEWIDTH, TILEWIDTH))
            img_list.append(img)
        return img_list

    #@staticmethod
    #def load_animals_list():
    #    img_list = []
    #    for i in range(1, 4):
    #        img_name = ANIMALS_1_3[0] + str(i) + ANIMALS_1_3[1]
    #        img = ImageManager.load(img_name)
    #        # resize?
    #        img = pg.transform.scale(img, (TILEWIDTH, TILEWIDTH))
    #        img_list.append(img)
    #    return img_list

    @staticmethod
    def load_landscape_list():
        img_list = []
        for i in range(1, 4):
            img_name = LANDSCAPE_1_3[0] + str(i) + LANDSCAPE_1_3[1]
            img = ImageManager.load(img_name)
            # resize?
            img = pg.transform.scale(img, (TILEWIDTH, TILEWIDTH))
            img_list.append(img)
        return img_list
