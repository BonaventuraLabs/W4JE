from src.player.player import Player
from collections import deque
from src.utilities.settings import *


class TurnManager:
    def __init__(self, game):
        self.game = game
        self.player_deque = deque([Player(self, 'Dimas', YELLOW),
                                   Player(self, 'Alex', RED),
                                   Player(self, 'Danila', GREEN)])

        self.current_player = self.player_deque[0]
        self.current_player.set_current()
        self.turn_finished = False

    def set_next_player(self):
        pass