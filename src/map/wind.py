import numpy as np


class Wind:

    def __init__(self, game):
        self.game = game
        # self.directions = {'N': 0, 'NW': 45, 'W': 90, 'SW': 135, 'S': 180, 'SE': 225, 'E': 270, 'NE': 315}
        # self.current_direction = 'N'

        self.directions = {'lu': 30, 'l': 90, 'ld': 150, 'rd': 210, 'r': 270, 'ru': 330}
        self.current_direction = np.random.choice(list(self.directions.keys()))
        self.current_angle = self.directions[self.current_direction]

        #self.strengths = [0, 1, 2, 3, 4]
        self.strengths = [2, 3, 4]
        self.current_strength = 3
        # 0 - shtil, 4 - storm?

        # ship movements are affected by wind:
        self.ship_movement_penalty_dict = {'lu': 0, 'l': 0, 'ld': 0, 'rd': 0, 'r': 0, 'ru': 0}
        self.update_movement_penalties()

    def update(self, *args):
        self.get_random_direction()

    def get_random_direction(self):
        #TODO: make process not completely random, but with bias to current state.
        # kind of: np.random.choice([1,2], p=[0.9, 0.1])
        self.current_direction = np.random.choice(list(self.directions.keys()))
        self.current_angle = self.directions[self.current_direction]
        self.current_strength = np.random.choice(self.strengths)
        self.update_movement_penalties()

    def update_movement_penalties(self):
        """
        Update penalties. If ship moves along the wind direction, no penalty: -1.
        If ship moves in the first neighbor direction: penalty is -2.
        If ship moves in the second neighbor direction: penalty is -3
        If ship moves in the opposite direction: penalty is -4.

        Hexagonal directions of wind:
        2nd neighbor     \  / 1st neighbor
        opposite       -- o --> wind
        2nd neighbor    /  \ 1st neighbor

        This implementation is too simple: strength is not taken into account #TODO.
        :return: Null.
        """
        # base values
        self.ship_movement_penalty_dict = {'lu': 0, 'l': 0, 'ld': 0, 'rd': 0, 'r': 0, 'ru': 0}

        # update. Can be done in a smarter way. Later.
        if self.current_direction == 'lu':
            self.ship_movement_penalty_dict['ru'] = -2
            self.ship_movement_penalty_dict['lu'] = -1
            self.ship_movement_penalty_dict['l'] = -2
            self.ship_movement_penalty_dict['ld'] = -3
            self.ship_movement_penalty_dict['rd'] = -4
            self.ship_movement_penalty_dict['r'] = -3
        elif self.current_direction == 'ru':
            self.ship_movement_penalty_dict['ru'] = -1
            self.ship_movement_penalty_dict['lu'] = -2
            self.ship_movement_penalty_dict['l'] = -3
            self.ship_movement_penalty_dict['ld'] = -4
            self.ship_movement_penalty_dict['rd'] = -3
            self.ship_movement_penalty_dict['r'] = -2
        elif self.current_direction == 'r':
            self.ship_movement_penalty_dict['ru'] = -2
            self.ship_movement_penalty_dict['lu'] = -3
            self.ship_movement_penalty_dict['l'] = -4
            self.ship_movement_penalty_dict['ld'] = -3
            self.ship_movement_penalty_dict['rd'] = -2
            self.ship_movement_penalty_dict['r'] = -1
        elif self.current_direction == 'rd':
            self.ship_movement_penalty_dict['ru'] = -3
            self.ship_movement_penalty_dict['lu'] = -4
            self.ship_movement_penalty_dict['l'] = -3
            self.ship_movement_penalty_dict['ld'] = -2
            self.ship_movement_penalty_dict['rd'] = -1
            self.ship_movement_penalty_dict['r'] = -2
        elif self.current_direction == 'ld':
            self.ship_movement_penalty_dict['ru'] = -4
            self.ship_movement_penalty_dict['lu'] = -3
            self.ship_movement_penalty_dict['l'] = -2
            self.ship_movement_penalty_dict['ld'] = -1
            self.ship_movement_penalty_dict['rd'] = -2
            self.ship_movement_penalty_dict['r'] = -3
        elif self.current_direction == 'l':
            self.ship_movement_penalty_dict['ru'] = -3
            self.ship_movement_penalty_dict['lu'] = -2
            self.ship_movement_penalty_dict['l'] = -1
            self.ship_movement_penalty_dict['ld'] = -2
            self.ship_movement_penalty_dict['rd'] = -3
            self.ship_movement_penalty_dict['r'] = -4
