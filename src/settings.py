import os

TILE_SEA_IMAGE = 'tile_sea_1.png'
TILE_LAND_IMAGE = 'tile_land_1.png'
FOLDER_RESOURCES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))


TITLE = 'W4JE'

WIDTH = 800
HEIGHT = 600


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (100, 100, 100)
BGCOLOR = LIGHTGREY


TILEHEIGHT = 32
TILEWIDTH = 28
TILER = TILEHEIGHT/2 # for vertical hexagons
TILECOLORKEY = (0, 0, 0) # alpha channel?...

FPS = 60