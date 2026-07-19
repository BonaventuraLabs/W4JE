# Windows quick start

The initial supported development environment is Windows 10 or Windows 11 with Python 3.11.

Open PowerShell in the repository root and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
.\run_game.ps1
```

If PowerShell blocks local scripts, allow them for the current PowerShell session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

The standard game uses `resources/map_1.txt` and requires only Pygame and NumPy. The older random-map generation functions use `scikit-image` as an optional dependency.

Attention - some changes made.
Battle added, move keys are different now, wind can't be zero strength to speed up testing


# W4JE
This is a a project of two friends who decided one day to learn python.
They wanted to learn object oriented programming with Python and what can serve better for this purpose than writing a good game?

Therefore we start!

Current controls:
Ship Movement:

 t    y
  \  /
f--  --h
  /  \
 v    b

These controls are better suited for hexagone moves

g - end of turn

Numpad Enter
end turn

Numpad 5:
center camera on ship

Numpad 0:
center camera on Castle

Key c:
collect item

Key i:
info on current ship

Key d:
debug mode.

THis update: 
1) Map generation based on txt file.
2) The generated map is now in the originally planned form.
3) Villages where gold can be picked up per user.
4) If a user stops by own village he gets gold and when he delivers gold back to the home base town it is counted. So, there is game winning situation now available.
5) Some new improved tile graphics (mountains, sand).

### Run automated tests

After completing the Windows quick-start setup, run:

```powershell
.\run_tests.ps1
```

The current tests validate the shared six-neighbour hex-grid coordinate rules used by human, AI and pirate ships.
