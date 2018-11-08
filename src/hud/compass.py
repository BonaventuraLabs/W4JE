import pygame as pg
from src.utilities.settings import *
from src.map.text import Text


class Compass(pg.sprite.Sprite):

    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        # self.image.fill((250, 250, 180))
        self.image = self.game.image_manager.hud_compass
        self.rect = self.image.get_rect()
        self.rect.center = (110, 230)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class WindArrow(pg.sprite.Sprite):
    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.image_manager.wind_arrow
        self.rect = self.image.get_rect()
        self.fixed_position = (110, 230)
        self.rect.center = self.fixed_position
        self.update()

    def update(self, *args):
        angle = self.game.atmosphere.wind.current_angle
        # self.game.wind.directions[self.game.wind.current_direction]
        # use ONLY the stock image for rotation.
        self.image = pg.transform.rotate(self.game.image_manager.wind_arrow, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.fixed_position

    def show_text(self):
        txt = Text(self.game)
        text = 'Wind strength: ' + str(self.game.atmosphere.wind.current_strength)
        txt.draw_text(text, 20, 110, 130)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        self.show_text()