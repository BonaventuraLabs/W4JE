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
        self.start_turn(self.player_deque[0])

        # self.turn_finished = False

    def start_turn(self, player):
        self.current_player = player
        self.current_player.is_current = True
        self.current_player.is_done = False
        self.current_player.ship.moves_left = self.current_player.ship.moves_per_turn
        self.current_player.ship.recalc_center()
        self.game.camera.update(self.current_player.ship.rect.x, self.current_player.ship.rect.y)

    def on_end_turn(self):
        self.current_player.is_current = False

    def check_state(self):
        # if the current player is a pirate:
        if isinstance(self.current_player, Pirate):
            pg.time.wait(1000)
            while self.current_player.ship.moves_left > 0:
                # TODO: pirate can move more than normal player, since moves_left is allowed to be negative.
                self.current_player.handle_move()
            else:
                self.current_player.is_done = True

        if not self.current_player.is_done:
            return

        # if player is done: end turn
        self.on_end_turn()

        # Generate next turn:
        PlayerTurnManager.global_turn_count += 1



        # go to next player; rotate player deck once
        self.player_deque.rotate(1)
        self.start_turn(self.player_deque[0])

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




