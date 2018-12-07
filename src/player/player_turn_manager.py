from src.player.player import Player
from src.player.ai_player import AI_Player
from src.player.ai_ship import AIship
from src.player.pirate import Pirate
from collections import deque
from src.utilities.settings import *
import pygame as pg


class PlayerTurnManager:

    # TODO: show this counter somewherein hud
    global_turn_count = 1

    def __init__(self, game):
        self.game = game
        if game.pname1 == 'Computer':
            p1 = AI_Player(self.game, game.pname1, YELLOW, 4, 25, 'English')
        else:
            p1 = Player(self.game, game.pname1, YELLOW, 4, 25, 'English')
        if game.pname2 == 'Computer':
            p2 = AI_Player(self.game, game.pname2, RED, 25, 4, 'Dutch')
        else:
            p2 = Player(self.game, game.pname2, RED, 25, 4, 'Dutch')
        if game.pname3 == 'Computer':
            p3 = AI_Player(self.game, game.pname3, GREEN, 25, 45, 'French')
        else:
            p3 = Player(self.game, game.pname3, GREEN, 25, 45, 'French')
        if game.pname4 == 'Computer':
            p4 = AI_Player(self.game, game.pname4, BLUE, 46, 25, 'Spanish')
        else:
            p4 = Player(self.game, game.pname4, BLUE, 46, 25, 'Spanish')
        p5 = Pirate(self.game, 'Black Beard', BLACK, 25, 25, 'English')

        self.player_deque = deque([p1, p2, p3, p4, p5])
        self.current_player = None
        self.current_ship = None
        self.start_turn(self.player_deque[0], self.player_deque[0].ships[0])

    def start_turn(self, player, ship):
        self.current_player = player
        self.current_player.is_current = True
        self.current_player.is_done = False
        self.current_ship = ship
        if not self.current_ship.destroyed:
            self.current_ship.is_current = True
            self.current_ship.is_done = False
            self.current_ship.moves_left = self.current_ship.moves_per_turn
            self.current_ship.recalc_center()
            self.game.camera.update(self.current_ship.rect.x, self.current_ship.rect.y)

    def on_end_turn(self):
        self.current_player.is_current = False

        # Generate next turn. It is actually pushing next player turn, not a new round of players turns.
        PlayerTurnManager.global_turn_count += 1

        # go to next player; rotate player deck once
        self.player_deque.rotate(1)
        self.start_turn(self.player_deque[0], self.player_deque[0].ships[0])

        # update things
        self.game.atmosphere.on_turn_end()
        self.game.hud.on_turn_end()

    def check_state(self):
        # if current player got winning score
        if not isinstance(self.current_player, Pirate):
            self.game.win_check(self.current_player)

        # if the current player is a pirate:
        if isinstance(self.current_player, Pirate):
            #pg.time.wait(1000)
            while self.current_ship.moves_left > 0:
                # TODO: pirate can move more than normal player, since moves_left is allowed to be negative.
                self.current_player.handle_move()
            else:
                self.current_player.is_done = True

        # if the current player is AI
        if isinstance(self.current_player, AI_Player):
            count = 0
            for sh in self.current_player.ships:
                if not sh.destroyed:
                    count += 1
            print('Gold in the ' + str(self.current_player.nation) + ' port: ' + str(self.current_player.castle.gold))
            print('Count of ' + str(self.current_player.nation) + ' ships: ' + str(count))
            if count < 3:
                if self.current_player.nation == 'English':
                    if self.current_player.castle.gold > 0:
                        self.current_player.ships.append(
                            AIship(self.game, self.current_player, self.current_player.row, self.current_player.col,
                                   'Sloop'))
                        self.current_player.castle.gold -= 1
                if self.current_player.nation == 'Dutch':
                    if self.current_player.castle.gold > 3:
                        self.current_player.ships.append(
                            AIship(self.game, self.current_player, self.current_player.row, self.current_player.col,
                                   'Frigate'))
                        self.current_player.castle.gold -= 3
                if self.current_player.nation not in ('Dutch', 'English'):
                    if self.current_player.castle.gold == 1:
                        self.current_player.ships.append(AIship(self.game, self.current_player, self.current_player.row, self.current_player.col, 'Sloop'))
                        self.current_player.castle.gold -= 1
                        print('Computer ' + str(self.current_player.nation) + ' bought a sloop')
                    elif self.current_player.castle.gold == 2:
                        self.current_player.ships.append(AIship(self.game, self.current_player, self.current_player.row, self.current_player.col, 'Brigantine'))
                        self.current_player.castle.gold -= 2
                        print('Computer ' + str(self.current_player.nation) + ' bought a brigantine')
                    elif  self.current_player.castle.gold > 2:
                        self.current_player.ships.append(AIship(self.game, self.current_player, self.current_player.row, self.current_player.col, 'Frigate'))
                        self.current_player.castle.gold -= 3
                        print('Computer ' + str(self.current_player.nation) + ' bought a frigate')

            while self.current_ship.moves_left > 0:
                #self.current_player.handle_move()
                self.current_ship.handle_move()
            else:
                #self.current_player.is_done = True
                self.current_ship.is_done = True

        # if the current ship is done check if it is players last ship and if yes pass turn to the next player
        if self.current_ship.is_done:
            self.current_ship.status = ''
            self.current_ship.is_current = False
            ind = self.current_player.ships.index(self.current_ship)
            if ind == len(self.current_player.ships)-1:
                self.current_player.is_done = True
                # if player is done: end turn
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

    def get_clicked(self, map_xy):
        clicked_item = None
        for player in self.player_deque:
            for sh in player.ships:
                if sh.rect.collidepoint(map_xy):
                    clicked_item = sh
                    clicked_item.on_click()
                break
            #if player != Pirate:
            if player.color != BLACK:
                if player.castle.rect.collidepoint(map_xy):
                    clicked_item = player.castle
                    clicked_item.on_click()
                    break
        return clicked_item




