"""Regression tests for defect #5: a move must not execute (and moves_left
must not go negative) when its wind-penalty cost exceeds the ship's
remaining moves_left. Covers PirateShip and AIship, which had the bug;
Ship (human) already had a correct check and is not touched.
"""
import unittest
from collections import deque

import pygame as pg

from src.player.pirate import PirateShip
from src.player.ai_ship import AIship
from src.map.hex_grid import get_neighbor


class StubWind:
    def __init__(self, penalty_dict, current_strength=3):
        self.ship_movement_penalty_dict = penalty_dict
        self.current_strength = current_strength


class StubAtmosphere:
    def __init__(self, wind):
        self.wind = wind


class StubTile:
    type = 'sea'


class StubMap:
    def get_tile_by_rc(self, r, c):
        return StubTile()

    def rc_to_xy(self, r, c):
        return (r * 10, c * 10)


class StubPlayerTurnManager:
    def __init__(self):
        self.player_deque = deque()


class StubGame:
    def __init__(self, penalty_dict):
        self.atmosphere = StubAtmosphere(StubWind(penalty_dict))
        self.map = StubMap()
        self.player_turn_manager = StubPlayerTurnManager()


def make_pirate_ship(moves_left, moves_per_turn, penalty_dict):
    ship = PirateShip.__new__(PirateShip)
    ship.game = StubGame(penalty_dict)
    ship.player = None
    ship.r = 10
    ship.c = 10
    ship.moves_left = moves_left
    ship.moves_per_turn = moves_per_turn
    ship.move_penalty = 0
    ship.destroyed = False
    ship.xy = (100, 100)
    ship.rect = pg.Rect(0, 0, 10, 10)
    ship.is_done = False
    ship.is_current = True
    return ship


def make_ai_ship(moves_left, moves_per_turn, penalty_dict):
    ship = AIship.__new__(AIship)
    ship.game = StubGame(penalty_dict)
    ship.player = None
    ship.ships_nation = 'French'  # skips the Dutch/Spanish target-scan branch
    ship.crew = 40
    ship.r = 10
    ship.c = 10
    ship.moves_left = moves_left
    ship.moves_per_turn = moves_per_turn
    ship.move_penalty = 0
    ship.destroyed = False
    ship.xy = (100, 100)
    ship.rect = pg.Rect(0, 0, 10, 10)
    ship.is_done = False
    ship.is_current = True
    return ship


class PirateShipMoveAffordabilityTests(unittest.TestCase):
    def test_move_costing_more_than_remaining_does_not_move_and_ends_turn(self):
        ship = make_pirate_ship(moves_left=2, moves_per_turn=12, penalty_dict={'l': -5})

        ship.analyze_move('l')

        self.assertEqual((ship.r, ship.c), (10, 10))
        self.assertEqual(ship.moves_left, 0)
        self.assertGreaterEqual(ship.moves_left, 0)
        self.assertTrue(ship.is_done)
        self.assertFalse(ship.is_current)

    def test_affordable_move_still_executes_normally(self):
        ship = make_pirate_ship(moves_left=10, moves_per_turn=12, penalty_dict={'l': -3})

        ship.analyze_move('l')

        self.assertEqual((ship.r, ship.c), get_neighbor(10, 10, 'l'))
        self.assertEqual(ship.moves_left, 7)


class AIshipMoveAffordabilityTests(unittest.TestCase):
    def test_move_costing_more_than_remaining_does_not_move_and_ends_turn(self):
        ship = make_ai_ship(moves_left=2, moves_per_turn=16, penalty_dict={'l': -5})

        ship.analyze_move((20, 20), 'l')

        self.assertEqual((ship.r, ship.c), (10, 10))
        self.assertEqual(ship.moves_left, 0)
        self.assertGreaterEqual(ship.moves_left, 0)
        self.assertTrue(ship.is_done)
        self.assertFalse(ship.is_current)

    def test_affordable_move_still_executes_normally(self):
        ship = make_ai_ship(moves_left=10, moves_per_turn=16, penalty_dict={'l': -3})

        ship.analyze_move((20, 20), 'l')

        self.assertEqual((ship.r, ship.c), (20, 20))
        self.assertEqual(ship.moves_left, 7)


if __name__ == "__main__":
    unittest.main()
