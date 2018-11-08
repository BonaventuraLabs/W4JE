import pygame as pg
from src.map.text import Text
from src.player.player_turn_manager import PlayerTurnManager


class ShipInfo(pg.sprite.Sprite):

    def __init__(self, game, hud):
        self.game = game

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
        rect.center = (110, 420)
        self.game.screen.blit(image, rect)
        self.show_text()

    def show_text(self):
        txt = Text(self.game)
        cur_player = self.game.player_turn_manager.current_player
        cur_ship = self.game.player_turn_manager.current_ship
        owner_rank = '%s %s' % (cur_player.name, cur_ship.rank)
        txt.draw_text(owner_rank, 20, 110, 510)
        moves = 'Moves: %s / %s ' % (cur_ship.moves_left, cur_ship.moves_per_turn)
        txt.draw_text(moves, 20, 110, 540)
        cl = 'Coordinates: ' + str(cur_ship.r) + '-' + str(cur_ship.c)
        txt.draw_text(cl, 20, 110, 570)
        cr = 'Crew ' + str(cur_ship.crew)
        txt.draw_text(cr, 20, 110, 600)
        gl = 'Attack ' + str(cur_ship.attack)
        txt.draw_text(gl, 20, 110, 630)
        gl = 'Gold ' + str(cur_ship.load)
        txt.draw_text(gl, 20, 110, 670)

