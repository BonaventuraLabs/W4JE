import unittest
from collections import deque

import pygame as pg

from src.player.player_turn_manager import PlayerTurnManager
from src.utilities.settings import BLACK, YELLOW


class StubClickable:
    """Minimal stand-in for Ship/Castle: only what get_clicked touches."""

    def __init__(self, rect):
        self.rect = rect
        self.click_count = 0

    def on_click(self):
        self.click_count += 1


class StubPlayer:
    def __init__(self, color, ships, castle_rect):
        self.color = color
        self.ships = ships
        self.castle = StubClickable(castle_rect)


def make_manager(players):
    # Bypass __init__ (which needs a full Game/Player/Ship graph); get_clicked
    # only reads self.player_deque, so a stubbed deque is sufficient.
    manager = PlayerTurnManager.__new__(PlayerTurnManager)
    manager.player_deque = deque(players)
    return manager


class GetClickedTests(unittest.TestCase):
    def setUp(self):
        self.ships = [
            StubClickable(pg.Rect(0, 0, 10, 10)),
            StubClickable(pg.Rect(100, 0, 10, 10)),
            StubClickable(pg.Rect(200, 0, 10, 10)),
        ]
        self.player = StubPlayer(YELLOW, self.ships, pg.Rect(900, 900, 10, 10))
        self.manager = make_manager([self.player])

    def test_clicking_first_ship_registers(self):
        clicked = self.manager.get_clicked((5, 5))
        self.assertIs(clicked, self.ships[0])
        self.assertEqual(self.ships[0].click_count, 1)
        self.assertEqual(self.ships[1].click_count, 0)
        self.assertEqual(self.ships[2].click_count, 0)

    def test_clicking_second_ship_registers(self):
        clicked = self.manager.get_clicked((105, 5))
        self.assertIs(clicked, self.ships[1])
        self.assertEqual(self.ships[1].click_count, 1)
        self.assertEqual(self.ships[0].click_count, 0)
        self.assertEqual(self.ships[2].click_count, 0)

    def test_clicking_third_ship_registers(self):
        clicked = self.manager.get_clicked((205, 5))
        self.assertIs(clicked, self.ships[2])
        self.assertEqual(self.ships[2].click_count, 1)
        self.assertEqual(self.ships[0].click_count, 0)
        self.assertEqual(self.ships[1].click_count, 0)

    def test_click_on_empty_water_returns_none(self):
        clicked = self.manager.get_clicked((5000, 5000))
        self.assertIsNone(clicked)
        self.assertTrue(all(sh.click_count == 0 for sh in self.ships))

    def test_pirate_castle_is_never_click_checked(self):
        # Pirates (color == BLACK) have no castle click handling. A click on
        # the pirate's castle coordinates, with no ship there, must miss.
        pirate_ship = StubClickable(pg.Rect(0, 0, 10, 10))
        pirate_castle_rect = pg.Rect(500, 500, 10, 10)
        pirate = StubPlayer(BLACK, [pirate_ship], pirate_castle_rect)
        manager = make_manager([pirate])

        clicked = manager.get_clicked((505, 505))

        self.assertIsNone(clicked)


if __name__ == "__main__":
    unittest.main()
