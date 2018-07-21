import pygame as pg
from src.Settings import *


class Hud:
    def __init__(self, game):
        self.game = game
        self.scroll = Scroll(game)
        self.compass = Compass(game)
        self.wind_arrow = WindArrow(game)
        self.turn_message = TurnMessage(game)

    def draw(self):
        self.scroll.draw()
        self.compass.draw()
        self.wind_arrow.draw()
        self.turn_message.draw()

    def update(self):
        pass


class Scroll(pg.sprite.Sprite):

    def __init__(self, game):
        self.game = game
        self.groups = game.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        # self.image.fill((250, 250, 180))
        self.image = self.game.image_manager.hud_scroll
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class Compass(pg.sprite.Sprite):

    def __init__(self, game):
        self.game = game
        self.groups = game.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        # self.image.fill((250, 250, 180))
        self.image = self.game.image_manager.hud_compass
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class WindArrow(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.sprites_hud, game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.image_manager.wind_arrow
        self.rect = self.image.get_rect()
        self.fixed_position = (100, 200)
        self.rect.center = self.fixed_position

    def update(self, *args):
        pass#self.get_new_direction()

    def show_text(self):
        text = 'Wind strength: ' + str(self.game.wind.current_strength)
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = self.game.hud.compass.rect.topleft
        self.game.screen.blit(label, label_rect)

    def draw(self):
        angle = self.game.wind.directions[self.game.wind.current_direction]
        # use ONLY the stock image for rotation.
        self.image = pg.transform.rotate(self.game.image_manager.wind_arrow, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.fixed_position
        self.game.screen.blit(self.image, self.rect)
        self.show_text()


class TurnMessage:
    def __init__(self, game):
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

        text = 'Coordinates: ' + str(self.game.current_player.r) + '-' + str(self.game.current_player.c)
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect(center=(100, HEIGHT / 2 + 20))
        self.game.screen.blit(label, label_rect)
