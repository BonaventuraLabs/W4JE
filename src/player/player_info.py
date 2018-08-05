import pygame as pg
from src.utilities.settings import *


class PlayerInfo:
    def __init__(self, game, hud):
        self.game = game
        self.image = pg.Surface((120, 60))
        self.image.fill((150, 120, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 310)

    def draw(self):

        # blit box:
        self.game.screen.blit(self.image, self.rect)

        # blit player info:
        cur_player = self.game.player_turn_manager.current_player
        cur_color = BLACK #cur_player.color

        info_str = '%s. moves: %s / %s '%(cur_player.name, cur_player.ship.moves_left, cur_player.ship.moves_per_turn)
        label_1 = self.game.font.render(info_str, True, cur_color)
        label_rect_1 = label_1.get_rect()
        label_rect_1.topleft = self.rect.topleft
        self.game.screen.blit(label_1, label_rect_1)

        text = 'Coordinates: ' + str(cur_player.ship.r) + '-' + str(cur_player.ship.c)
        label_2 = self.game.font.render(text, True, BLACK)
        label_rect_2 = label_2.get_rect()
        label_rect_2.left = self.rect.left
        label_rect_2.top = label_rect_1.bottom
        self.game.screen.blit(label_2, label_rect_2)

