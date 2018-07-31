import pygame as pg
from src.utilities.settings import *
from src.hud.scroll import Scroll
from src.hud.minimap import Minimap
from src.hud.button_end_turn import ButtonEndTurn
from src.hud.compass import Compass, WindArrow
from src.player.player_info import PlayerInfo

class Hud:
    def __init__(self, game):
        self.game = game
        self.sprites_hud = pg.sprite.Group()
        self.sprites_hud_clickable = pg.sprite.Group()
        self.scroll = Scroll(game, self)
        self.compass = Compass(game, self)
        self.wind_arrow = WindArrow(game, self)
        self.player_info = PlayerInfo(game, self)
        self.minimap = Minimap(game, self)
        self.turn_end_button = ButtonEndTurn(game, self)

    def draw(self):
        self.scroll.draw()
        self.compass.draw()
        self.wind_arrow.draw()
        self.player_info.draw()
        self.minimap.draw()
        self.turn_end_button.draw()

    def on_turn_end(self):
        #TODO: update all the time the hud??? For example - map updates independently of turns.
        self. wind_arrow.update()

    def get_clicked(self, screen_xy):
        clicked_item = None
        for sprite in self.sprites_hud_clickable:
            if sprite.rect.collidepoint(screen_xy):
                clicked_item = sprite
                clicked_item.on_click()
                break

        if clicked_item is None:
            # test the rest items in the hud:
            for sprite in self.sprites_hud:
                if sprite.rect.collidepoint(screen_xy):
                    clicked_item = sprite
                    break

        return clicked_item




