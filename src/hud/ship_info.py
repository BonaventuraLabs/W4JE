import pygame as pg
from src.map.text import Text
from src.utilities.settings import *


class ShipInfo(pg.sprite.Sprite):

    def __init__(self, game, hud):
        self.game = game
        self.upperloc = 300
        self.groups = hud.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)

    def draw(self):
        cur_ship = self.game.player_turn_manager.current_ship
        if cur_ship.rank == 'Sloop':
            image = self.game.image_manager.sloophud
        elif cur_ship.rank == 'Brigantine':
            image = self.game.image_manager.brigantinehud
        else:
            image = self.game.image_manager.frigatehud
        rect = image.get_rect()
        rect.center = (110, self.upperloc)

        pct = cur_ship.crew / cur_ship.max_crew
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(55, self.upperloc + 80, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(55, self.upperloc + 80, fill, BAR_HEIGHT)
        pg.draw.rect(self.game.screen, GREEN, fill_rect)
        pg.draw.rect(self.game.screen, WHITE, outline_rect, 2)

        self.game.screen.blit(image, rect)
        self.show_text()

    def show_text(self):
        txt = Text(self.game)
        cur_player = self.game.player_turn_manager.current_player
        cur_ship = self.game.player_turn_manager.current_ship
        owner_rank = '%s %s' % (cur_player.name, cur_ship.rank)
        txt.draw_text(owner_rank, 20, 110, self.upperloc + 90)
        moves = 'Moves: %s / %s ' % (cur_ship.moves_left, cur_ship.moves_per_turn)
        txt.draw_text(moves, 20, 110, self.upperloc + 115)
        cl = 'Coordinates: ' + str(cur_ship.r) + '-' + str(cur_ship.c)
        txt.draw_text(cl, 20, 110, self.upperloc + 140)
        cr = 'Crew ' + str(cur_ship.crew)
        txt.draw_text(cr, 20, 110, self.upperloc + 165)
        gl = 'Attack ' + str(cur_ship.attack)
        txt.draw_text(gl, 20, 110, self.upperloc + 190)
        gl = 'Gold ' + str(cur_ship.load)
        txt.draw_text(gl, 20, 110, self.upperloc + 215)

    def draw_bar(self):
        cur_ship = self.game.player_turn_manager.current_ship
        pct = cur_ship.crew * 100 / cur_ship.max_crew
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(55, self.upperloc + 80, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(55, self.upperloc + 80, fill, BAR_HEIGHT)
        pg.draw.rect(self, GREEN, fill_rect)
        pg.draw.rect(self, WHITE, outline_rect, 2)

