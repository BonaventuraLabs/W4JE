import pygame as pg
from src.settings import *

class ImageLoader:
    def __init__(self, game):
        self.game = game
        self.sea_1 = ImageLoader.load(TILE_SEA_IMAGE)
        self.land_1 = ImageLoader.load(TILE_LAND_IMAGE)

    @staticmethod
    def load(name):
        return pg.image.load(os.path.join(FOLDER_RESOURCES, name)).convert_alpha()


