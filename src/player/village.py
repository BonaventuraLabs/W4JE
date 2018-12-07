import pygame as pg
from src.utilities.settings import *
import numpy as np


class Village(pg.sprite.Sprite):
    def __init__(self, game, player, row, col):
        self.game = game
        self.player = player
        self.groups = self.game.sprites_unit
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.image_manager.village

        self.rect = self.image.get_rect()
        self.r = row
        self.c = col
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))
        label, label_rect = self.get_name_label()
        self.game.screen.blit(label, self.game.camera.apply(label_rect))

    def get_name_label(self):
        if self.player.name == 'Computer':
            text = self.player.nation
        else:
            text = self.player.name
        label = self.game.font.render(text, True, WHITE)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        label_rect.bottom = self.rect.bottom
        return label, label_rect

    def on_click(self):
        print('\nClick : ' + self.player.name + ' castle')

    def print_full_info(self):
        print('---=== CASTLE ===---')
        print('Empty.')