import unittest

from src.map.hex_grid import get_neighbor, get_neighbors, hex_distance


class HexGridTests(unittest.TestCase):
    def test_even_row_neighbors_match_existing_movement_rules(self):
        self.assertEqual(
            set(get_neighbors(2, 2)),
            {(2, 1), (2, 3), (1, 1), (1, 2), (3, 1), (3, 2)},
        )

    def test_odd_row_neighbors_match_existing_movement_rules(self):
        self.assertEqual(
            set(get_neighbors(3, 2)),
            {(3, 1), (3, 3), (2, 2), (2, 3), (4, 2), (4, 3)},
        )

    def test_boundary_filter_removes_coordinates_outside_map(self):
        self.assertEqual(set(get_neighbors(0, 0, row_count=5, column_count=5)), {(0, 1), (1, 0)})

    def test_neighbor_relationship_is_symmetric(self):
        origin = (4, 4)
        for neighbor in get_neighbors(*origin):
            self.assertIn(origin, get_neighbors(*neighbor))

    def test_hex_distance(self):
        self.assertEqual(hex_distance((2, 2), (2, 2)), 0)
        self.assertEqual(hex_distance((2, 2), get_neighbor(2, 2, "lu")), 1)
        self.assertEqual(hex_distance((0, 0), (4, 2)), 4)

    def test_unknown_direction_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown hex direction"):
            get_neighbor(1, 1, "up")

    def test_partial_dimensions_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "provided together"):
            get_neighbors(1, 1, row_count=5)


if __name__ == "__main__":
    unittest.main()
