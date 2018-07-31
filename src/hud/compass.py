import pygame as pg
from src.utilities.settings import *


class Compass(pg.sprite.Sprite):

    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        # self.image.fill((250, 250, 180))
        self.image = self.game.image_manager.hud_compass
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class WindArrow(pg.sprite.Sprite):
    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.image_manager.wind_arrow
        self.rect = self.image.get_rect()
        self.fixed_position = (100, 200)
        self.rect.center = self.fixed_position

    def update(self, *args):
        angle = self.game.atmosphere.wind.current_angle
        # self.game.wind.directions[self.game.wind.current_direction]
        # use ONLY the stock image for rotation.
        self.image = pg.transform.rotate(self.game.image_manager.wind_arrow, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.fixed_position

    def show_text(self):
        text = 'Wind strength: ' + str(self.game.atmosphere.wind.current_strength)
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = self.game.hud.compass.rect.topleft
        self.game.screen.blit(label, label_rect)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        self.show_text()