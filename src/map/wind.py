import numpy as np


class Wind:
    def __init__(self, game):
        self.game = game
        self.directions = {'N': 0, 'NW': 45, 'W': 90, 'SW': 135, 'S': 180, 'SE': 225, 'E': 270, 'NE': 315}
        self.current_direction = 'N'
        self.current_angle = 0
        self.strengths = [0, 1, 2, 3, 4]
        self.current_strength = 3
        # 0 - shtil, 4 - storm.

    def update(self, *args):
        self.get_random_direction()

    def get_random_direction(self):
        self.current_direction = np.random.choice(list(self.directions.keys()))
        self.current_angle = self.directions[self.current_direction]
        self.current_strength = np.random.choice(self.strengths)
        # print(self.current_direction)

