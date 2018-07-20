import pygame as pg
from src.settings import *
from src.Units import Ship
import os
import numpy as np

vec = pg.math.Vector2


class Map:
    def __init__(self, game):
        self.game = game
        file_path = os.path.join(FOLDER_RESOURCES, 'map_1.txt')
        self.data = []
        with open(file_path, 'rt') as f:
            for line in f:
                self.data.append(line)
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)

        #TODO: wrong. height is not N*y, because the tiles are shifted
        self.height = self.tileheight * TILEHEIGHT
        self.width = self.tilewidth * TILEWIDTH
        self.tiles_dict = self.generate_tiles()

    def draw(self):
        pass

    def update(self):
        pass

    def generate_tiles(self):
        tile_dict = {}
        for row, tiles in enumerate(self.data):
            for col, el in enumerate(tiles):
                if el == '1':
                    tile_type = 'land'
                elif el == '.':
                    tile_type = 'sea'
                # elif el == 'P':
                #     self.game.ship = Ship(self.game, row, col)
                else:
                    tile_type = 'sea'

                tile_dict[str(row) + '.' + str(col)] = Tile(self.game, row, col, tile_type)
        return tile_dict


class Tile(pg.sprite.Sprite):
    def __init__(self, game, row, col, tile_type):
        self.type = tile_type
        self.groups = game.map_sprites, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.type == 'sea':
            self.image = self.game.images.sea_1
        elif self.type == 'land':
            self.image = self.game.images.land_1
        else:
            self.image = self.game.images.sea_1

        self.rect = self.image.get_rect()

        self.c = col
        self.r = row
        self.rc_str = str(self.r) + ', ' + str(self.c)

        # recalculate x, y
        self.center = Tile.recalculate_xy(self.r, self.c)
        self.rect.center = self.center

    @staticmethod
    def recalculate_xy(r, c):
        rx = TILER * np.cos(np.pi / 6)
        ry = TILER

        # real coordinates on map;
        # shift to right each 2nd row
        if r % 2 == 0:
            x = c * 2 * rx
            y = r * 1.5 * ry
        else:
            x = c * 2 * rx + rx  # here we shift to right.
            y = r * 1.5 * ry
        return x, y


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.speed = CAMERA_SPEED

    def apply(self, target):
        return target.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        self.camera = pg.Rect(x, y, self.width, self.height)

    def check_key_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.camera.x += self.speed
        if keys[pg.K_RIGHT]:
            self.camera.x -= self.speed
        if keys[pg.K_UP]:
            self.camera.y += self.speed
        if keys[pg.K_DOWN]:
            self.camera.y -= self.speed
        # self.camera = pg.Rect(x, y, self.width, self.height)

class Wind(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.top_layer_sprites, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.images.wind_arrow_1
        self.directions = {'N':0, 'NW':45, 'W':90, 'SW': 135, 'S':180, 'SE':225, 'E':270, 'NE':315}
        self.current_direction = 'N'
        self.strengths = [0, 1, 2, 3, 4]
        self.current_strength = 0
        self.rect = self.image.get_rect()
        # recalculate x, y
        self.fixed_position = (50, HUD_HEIGHT/2)
        self.rect.center = self.fixed_position
        # 0 - shtil, 4 - storm.

    def update(self, *args):
        pass#self.get_new_direction()

    def show_text(self):
        label = self.game.font.render(str(self.current_strength), True, BLACK)
        label_rect = label.get_rect(center=self.fixed_position)
        self.game.screen.blit(label, label_rect)


    def get_new_direction(self):
        self.current_direction = np.random.choice(list(self.directions.keys()))
        # print(self.current_direction)
        angle = self.directions[self.current_direction]
        # use the stock image for rotation!!!
        self.image = pg.transform.rotate(self.game.images.wind_arrow_1, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.fixed_position
        self.current_strength = np.random.choice(self.strengths)
