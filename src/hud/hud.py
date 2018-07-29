import pygame as pg
from src.utilities.settings import *
from src.hud.scroll import Scroll
from src.hud.minimap import Minimap
from src.hud.button_end_turn import ButtonEndTurn
from src.hud.compass import Compass, WindArrow


class Hud:
    def __init__(self, game):
        self.game = game
        self.sprites_hud = pg.sprite.Group()
        self.sprites_hud_clickable = pg.sprite.Group()
        self.scroll = Scroll(game, self)
        self.compass = Compass(game, self)
        self.wind_arrow = WindArrow(game, self)
        self.turn_message = TurnMessage(game, self)
        self.minimap = Minimap(game, self)
        self.turn_end_button = ButtonEndTurn(game, self)

    def draw(self):
        self.scroll.draw()
        self.compass.draw()
        self.wind_arrow.draw()
        self.turn_message.draw()
        self.minimap.draw()
        self.turn_end_button.draw()

    def update(self):
        pass

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


class TurnMessage:
    def __init__(self, game, hud):
        self.game = game
        self.image = pg.Surface((120, 60))
        self.image.fill((150, 120, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 310)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        label = self.game.font.render('Turn: ' + self.game.current_player.name, True, self.game.current_player.color)
        label_rect = label.get_rect(center=(100, HEIGHT / 2))
        self.game.screen.blit(label, label_rect)

        text = 'Coordinates: ' + str(self.game.current_player.ship.r) + '-' + str(self.game.current_player.ship.c)
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect(center=(100, HEIGHT / 2 + 20))
        self.game.screen.blit(label, label_rect)




