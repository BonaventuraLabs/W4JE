import os


SHEEP_SPEED = 10  # moves (1 tile) per turn
TITLE = 'W4JE'

WIDTH = 1000
HEIGHT = 800
MAP_TILE_H = 50
MAP_TILE_W = 100

CAMERA_SPEED = 15 #pix
HUD_HEIGHT = 80

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (100, 100, 100)
BGCOLOR = LIGHTGREY
YELLOW = (255, 255, 0)

# original stile size: (w=28, h = 32)
TILEHEIGHT = 64 #32
TILEWIDTH = 56 #28
TILE_HEX_R = TILEHEIGHT/2 # for vertical hexagons
TILECOLORKEY = (0, 0, 0) # alpha channel?...

FPS = 60

SEAGULL_COUNT = 50
CLOUD_COUNT = 50

'''Resources'''
FOLDER_RESOURCES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))
TILE_SEA_IMAGE = 'tile_sea_1.png'
TILE_LAND_IMAGE = 'tile_land_1.png'
TILE_MOUNTAIN_IMAGE = 'tile_mountain_1.png'
TILE_SAND_IMAGE = 'tile_sand_1.png'

WIND_ARROW = 'wind_arrow_2.png'
HUD_SCROLL = 'hud_scroll_2.png'
HUD_COMPASS = 'hud_compass_3.png'
SHIP = 'ship_1.png'
PIRATE = 'image_pirate_1.png'
SHIP_WRECK = 'image_ship_wreck_1.png'
SEAGULL = 'image_seagull_1.png'
CASTLE = 'image_castle_1.png'

CLOUDS_1_6 = ['image_cloud_', '.png']
FISH_1_2 = ['image_fish_', '.png']
ANIMALS_1_3 = ['image_animal_', '.png']


TILE_TYPE_DICT = {0: 'sea', 'sea': 0,
                  1: 'land', 'land': 1,
                  2: 'sand', 'sand': 2,
                  3: 'mountain', 'mountain': 3}

