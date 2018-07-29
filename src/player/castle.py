import pygame as pg
from src.utilities.settings import *
import numpy as np


class Castle(pg.sprite.Sprite):
    def __init__(self, game, player, row, col):
        self.game = game
        self.player = player
        self.groups = self.game.sprites_unit, self.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.image_manager.castle

        self.rect = self.image.get_rect()
        self.r = row
        self.c = col
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))
        self.game.screen.blit(self.get_name_label(), self.game.camera.apply(self))

    def get_name_label(self):
        text = self.player.name
        label = self.game.font.render(text, True, BLACK)
        label.get_rect().center = self.rect.center
        label.get_rect().bottom = self.rect.bottom
        return label