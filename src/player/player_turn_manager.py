from src.player.player import Player
from src.player.pirate import Pirate
from collections import deque
from src.utilities.settings import *
import pygame as pg


class PlayerTurnManager:

    # TODO: show this counter somewherein hud
    global_turn_count = 1

    def __init__(self, game):
        self.game = game
        self.player_deque = deque([Player(self.game, 'Dimas', YELLOW),
                                   Player(self.game, 'Alex', RED),
                                   Player(self.game, 'Danila', GREEN),
                                   Pirate(self.game, 'Long John', BLACK)])
        self.current_player = None
        self.current_ship = None
        self.start_turn(self.player_deque[0], self.player_deque[0].ships[0])

        # self.turn_finished = False

    def start_turn(self, player, ship):
        self.current_player = player
        self.current_player.is_current = True
        self.current_player.is_done = False
        self.current_ship = ship
        self.current_ship.is_current = True
        self.current_ship.is_done = False
        self.current_ship.moves_left = self.current_ship.moves_per_turn
        self.current_ship.recalc_center()
        if not self.current_ship.destroyed:
            self.game.camera.update(self.current_ship.rect.x, self.current_ship.rect.y)


    def on_end_turn(self):
        self.current_player.is_current = False

        # Generate next turn:
        PlayerTurnManager.global_turn_count += 1

        # go to next player; rotate player deck once
        self.player_deque.rotate(1)
        self.start_turn(self.player_deque[0], self.player_deque[0].ships[0])

        # update things
        self.game.atmosphere.on_turn_end()
        self.game.hud.on_turn_end()

    def check_state(self):

        # if the current player is a pirate:
        if isinstance(self.current_player, Pirate):
            #pg.time.wait(1000)
            while self.current_ship.moves_left > 0:
                # TODO: pirate can move more than normal player, since moves_left is allowed to be negative.
                self.current_player.handle_move()
            else:
                self.current_player.is_done = True

        # if the current ship is done check if it is players last ship and if yes pass turn to the next player
        if self.current_ship.is_done:
            self.current_ship.is_current = False
            ind = self.current_player.ships.index(self.current_ship)
            if ind == len(self.current_player.ships)-1:
                self.current_player.is_done = True
                # if player is done: end turn
                print('PLAYER IS DONE')
                self.on_end_turn()


                return
            self.current_ship = self.current_player.ships[ind + 1]
            self.current_ship.is_current = True
            self.current_ship.is_done = False
            self.current_ship.moves_left = self.current_ship.moves_per_turn
            self.current_ship.recalc_center()
            self.game.camera.update(self.current_ship.rect.x, self.current_ship.rect.y)

        if not self.current_player.is_done:
            return

        # if player is done: end turn
        self.on_end_turn()

        # update things
        self.game.atmosphere.on_turn_end()
        self.game.hud.on_turn_end()



    def get_clicked(self, map_xy):
        clicked_item = None
        for player in self.player_deque:
            if player.ship.rect.collidepoint(map_xy):
                clicked_item = player.ship
                clicked_item.on_click()
                break
            if player.castle.rect.collidepoint(map_xy):
                clicked_item = player.castle
                clicked_item.on_click()
                break
        return clicked_item




