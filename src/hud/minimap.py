from src.map.map_generator import MapGenerator
import pygame as pg


class Minimap(pg.sprite.Sprite):
    def __init__(self, game, hud):
        self.id = 'minimap'
        self.game = game
        self.groups = hud.sprites_hud_clickable
        pg.sprite.Sprite.__init__(self, self.groups)

        # get map image
        image = MapGenerator.generate_minimap(self.game.map.tiles_dict,
                                              self.game.map.height_in_tiles,
                                              self.game.map.width_in_tiles)

        # rescale size:
        target_width = 120
        target_height = int(image.get_rect().h / image.get_rect().w * target_width)

        self.image = pg.transform.scale(image, (target_width, target_height))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 460)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        pass

    def on_click(self):
        print('Click : Minimap' )
