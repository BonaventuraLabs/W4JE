import os

'''Resources'''
FOLDER_RESOURCES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
TILE_SEA_IMAGE = 'tile_sea_1.png'
TILE_LAND_IMAGE = 'tile_land_1.png'
WIND_ARROW = 'wind_arrow_2.png'
HUD_SCROLL = 'hud_scroll_2.png'
HUD_COMPASS = 'hud_compass_1.png'
SHIP = 'ship_1.png'

TITLE = 'W4JE'

WIDTH = 800
HEIGHT = 600

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
TILER = TILEHEIGHT/2 # for vertical hexagons
TILECOLORKEY = (0, 0, 0) # alpha channel?...

FPS = 60