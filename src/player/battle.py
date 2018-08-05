import pygame as pg


class Battle:
    def __init__(self, attacking_ship, defending_ship):
        self.a_ship = attacking_ship
        self.d_ship = defending_ship

    def calculate_damage(self):
        # For now: simply destroy. TODO: make real battle.
        self.d_ship.make_destroyed()

    def start(self):
        print(self.a_ship)
        print('attacks')
        print(self.d_ship)
        self.calculate_damage()

