import pygame as pg
from src.utilities.settings import *


class ButtonEndTurn(pg.sprite.Sprite):
    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_hud, hud.sprites_hud_clickable
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.Surface((120, 40))
        self.image.fill((255,128,0))
        self.rect = self.image.get_rect()
        self.rect.center = (110, 750)
        self.id = 'end_turn_button'

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

        text = 'End Turn'
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        self.game.screen.blit(label, label_rect)

    def on_click(self):
        print('Click')
        self.game.player_turn_manager.current_ship.is_done = True
        self.game.player_turn_manager.current_ship.is_current = False
        self.game.player_turn_manager.current_ship.moves_left = 0


