import pygame as pg
from src.map.text import Text
from src.utilities.settings import *


class BottomHud:
    def __init__(self, game):
        self.game = game
        self.sprites_bottom_hud = pg.sprite.Group()
        self.bottom_scroll = BottomScroll(game, self)

    def draw(self):
        self.bottom_scroll.draw()


class BottomScroll(pg.sprite.Sprite):

    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_bottom_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.image_manager.bottom_scroll
        self.rect = self.image.get_rect()
        self.rect.topleft = (300, 680)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        self.show_text()

    def show_text(self):
        txt = Text(self.game)
        cur_ship = self.game.player_turn_manager.current_ship
        text = cur_ship.status
        txt.draw_text(text, 20, 700, 730)


