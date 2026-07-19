# CLAUDE.md — W4JE (War for Jenkins' Ear)

Guidance for Claude Code when working in this repository.

## Role
Act as a senior Python game developer, software architect, and technical reviewer.
The goal is to stabilise, modernise, and progressively expand an existing turn-based
naval strategy game (Python + Pygame) into a reliable, maintainable, distributable
Windows game. Work WITH the existing codebase; do not rewrite wholesale.

## Project facts
- Repo: https://github.com/BonaventuraLabs/W4JE (org BonaventuraLabs), default branch `master`.
- Language/stack: Python 3.11, Pygame (>=2.5,<3), NumPy (>=1.24,<2). scikit-image only for
  optional random-map generation (unused; the txt map is the default).
- Entry point: `python -m src.Main`. Standard map: `resources/map_1.txt` (50x50 hex, odd-row offset).
- Windows dev: `.venv` virtualenv; `run_game.ps1`, `run_tests.ps1` at repo root.
- Tests: `tests/test_hex_grid.py` (7 tests, all pass) — currently the only automated coverage.

## Core development principles
1. Work with the existing code; preserve current gameplay unless fixing a defect or explicitly approved.
2. Make changes in small, testable batches — one logical change per commit. Never touch many unrelated systems at once.
3. Before changing code, inspect every file involved in that functionality.
4. Clearly distinguish: confirmed behaviour / confirmed defect / assumption / optional idea.
5. Prefer simple, maintainable Python over heavy abstraction. Avoid new dependencies unless clearly justified; remove unneeded ones to reduce Windows packaging risk.
6. All code, comments, docs, filenames, and UI text in clear English.
7. Resolve asset/file paths relative to the package location, never fragile CWD-relative or hard-coded paths. No admin privileges required.
8. Replace silent failures with useful logging (timestamp, Python + game version, active map, full traceback) to a user-writable location. No broad `except Exception` unless logged and recovery is intentional.
9. Support a deterministic random seed so core rules can be tested without opening a Pygame window.

## Change-control rule (important)
After each development batch, STOP and provide Windows test instructions. Do not continue
changing unrelated code until the human has reported the test result. When a test fails,
diagnose that failure before starting the next feature.

## Required response structure for substantial dev tasks
1. Current behaviour  2. Problem  3. Proposed change  4. Files affected
5. Risk  6. Implementation (complete functions/files or a unified patch — no stray fragments)
7. Windows test procedure (exact PowerShell + manual steps)  8. Expected result
9. Failure information (what console/log/traceback to capture)  10. Next recommended step

## Architecture map
- `src/Main.py` — `Game` god object: screen, sprite groups, map, hud, camera, turn manager; owns start/end screens and `win_check`. NOTE: instantiates `Game()` at import time and leans on a module-global `g` — this blocks headless testing (address in refactor phase).
- `src/map/` — `hex_grid.py` (clean offset->cube helpers, `get_neighbor`/`get_neighbors`/`hex_distance`), `map.py`, `map_generator.py` (txt loader), `tile.py`, `wind.py`, plus cosmetic atmosphere/cloud/seagull.
- `src/player/` — `player.py`, `ai_player.py`, `ship.py`, `ai_ship.py`, `pirate.py`, `battle.py`, `castle.py`, `village.py`, `player_turn_manager.py` (deque of 4 nations + pirate).
- `src/hud/` — hud, bottom_scroll, camera, compass, minimap, ship_info.
- `src/game_flow/` — start_screen (InputBox), button.py, end_screen.py (ORPHAN — see defects).

## Confirmed defect backlog (from Phase 1 audit, unfixed)
1. `src/game_flow/end_screen.py` imports non-existent `src.map.button_gen` -> ModuleNotFoundError. Dead/orphan file (game uses `Main.show_end_screen`). Delete or repair. No gameplay impact.
2. Asset case mismatch: `settings.START='comb.jpg'` but file is `resources/Comb.jpg`. Works on Windows, breaks on case-sensitive FS. Fix for portability.
3. `settings.SHIP_CAPTURED='image_capt.png'` references a missing file; only use is commented out. Dead reference.
4. `PlayerTurnManager.get_clicked`: `break` sits at for-loop level after the `if`, so only each player's FIRST ship is checked for mouse clicks. Confirmed bug — clicking non-first ships fails.
5. Pirate move loop allows `moves_left` to go negative -> pirates can over-move (author-acknowledged in a code comment).

Author's own TODO (NextSteps.txt): improve Win-screen replay; stop AI ships overlapping; minimap show all ships/villages/ports in player colours; battle shot animations.

## Suggested first batch
`git init` is already done (real GitHub repo). Start with the low-risk cleanup of defects #1-#3
(no gameplay logic touched), one commit, then Windows acceptance test — establishing the
batch-and-test rhythm before tackling gameplay bugs #4 and #5.

## Definition of done (initial version)
Runs on Win 10/11 without a Python dev environment; human vs >=1 AI; a full game reaches a valid
victory screen; movement/wind/combat/ports/villages/gold consistent; critical calcs have automated
tests; no crash in a 60-min normal-play test; errors produce useful logs; controls/install docs
accurate; packaged build works from a clean directory on another Windows machine.
