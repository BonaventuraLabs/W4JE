"""Hex-grid coordinate helpers used by movement and future pathfinding.

W4JE uses an odd-row offset layout: odd-numbered rows are shifted to the
right. Coordinates are represented as ``(row, column)`` tuples.
"""

from __future__ import annotations

Coordinate = tuple[int, int]

# Keep the direction names already used by Ship, AIship and PirateShip.
_DIRECTION_DELTAS: dict[int, dict[str, Coordinate]] = {
    0: {  # even row
        "l": (0, -1),
        "r": (0, 1),
        "lu": (-1, -1),
        "ru": (-1, 0),
        "ld": (1, -1),
        "rd": (1, 0),
    },
    1: {  # odd row, shifted right
        "l": (0, -1),
        "r": (0, 1),
        "lu": (-1, 0),
        "ru": (-1, 1),
        "ld": (1, 0),
        "rd": (1, 1),
    },
}


def get_neighbor(row: int, column: int, direction: str) -> Coordinate:
    """Return the adjacent coordinate in ``direction``.

    Valid directions are ``l``, ``r``, ``lu``, ``ru``, ``ld`` and ``rd``.
    """

    try:
        row_delta, column_delta = _DIRECTION_DELTAS[row & 1][direction]
    except KeyError as exc:
        valid = ", ".join(_DIRECTION_DELTAS[0])
        raise ValueError(
            f"Unknown hex direction {direction!r}. Expected one of: {valid}."
        ) from exc

    return row + row_delta, column + column_delta


def get_neighbors(
    row: int,
    column: int,
    *,
    row_count: int | None = None,
    column_count: int | None = None,
) -> tuple[Coordinate, ...]:
    """Return the six adjacent coordinates, optionally clipped to map bounds."""

    coordinates = (
        get_neighbor(row, column, "l"),
        get_neighbor(row, column, "r"),
        get_neighbor(row, column, "lu"),
        get_neighbor(row, column, "ru"),
        get_neighbor(row, column, "ld"),
        get_neighbor(row, column, "rd"),
    )

    if row_count is None and column_count is None:
        return coordinates

    if row_count is None or column_count is None:
        raise ValueError("row_count and column_count must be provided together.")
    if row_count < 0 or column_count < 0:
        raise ValueError("Map dimensions cannot be negative.")

    return tuple(
        coordinate
        for coordinate in coordinates
        if _is_within_bounds(coordinate, row_count, column_count)
    )


def hex_distance(start: Coordinate, end: Coordinate) -> int:
    """Return the minimum number of hex steps between two coordinates."""

    start_cube = _offset_to_cube(*start)
    end_cube = _offset_to_cube(*end)
    return max(abs(a - b) for a, b in zip(start_cube, end_cube))


def _offset_to_cube(row: int, column: int) -> tuple[int, int, int]:
    """Convert odd-row offset coordinates to cube coordinates."""

    cube_x = column - (row - (row & 1)) // 2
    cube_z = row
    cube_y = -cube_x - cube_z
    return cube_x, cube_y, cube_z


def _is_within_bounds(
    coordinate: Coordinate, row_count: int, column_count: int
) -> bool:
    row, column = coordinate
    return 0 <= row < row_count and 0 <= column < column_count
