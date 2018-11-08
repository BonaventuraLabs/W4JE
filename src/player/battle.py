import pygame as pg
import random


class Battle:
    def __init__(self, attacking_ship, defending_ship):
        self.a_ship = attacking_ship
        self.d_ship = defending_ship

    def calculate_damage(self):

        v1 = self.a_ship.attack
        v2 = self.d_ship.attack

        x = random.randint(1, 10)
        print('random = ' + str(x))
        if x > 5:  # attacking ship lost
            self.a_ship.crew -= v2
            print('attacker minus ' + str(v2))
        else:
            self.d_ship.crew -= v1
            print('defender minus ' + str(v1))
        if self.a_ship.crew <= 0:
            self.a_ship.make_destroyed()
        if self.d_ship.crew <= 0:
            self.d_ship.make_destroyed()

    def start(self):
        print(self.a_ship)
        print('attacks')
        print(self.d_ship)
        self.calculate_damage()

