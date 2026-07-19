W4JE - WAR FOR JENKINS' EAR
PLAYER GUIDE
===========================

Version note
------------
W4JE is a playable development prototype written in Python with Pygame.
Some interfaces and AI functions are still under development. This guide
explains the controls and rules currently implemented in the source code.


1. GAME OVERVIEW
================

W4JE is a turn-based naval strategy game played on a large hexagonal map.
Four European nations compete for gold and naval supremacy:

- English
- Dutch
- French
- Spanish

A fifth faction, the pirates led by Black Beard, is controlled by the game.

Each nation owns:

- one home castle and port;
- two gold-producing villages;
- two Sloops;
- one Brigantine.

Players sail between ports and villages, collect gold, fight enemy ships,
collect random items from the sea, repair their fleet and purchase new ships.

The game can contain human and computer-controlled nations. On the start
screen, enter a player name for a human-controlled nation. Enter the exact
word "Computer" to let the AI control that nation.

The victory target can be set between 3 and 10 gold. Values below 3 or above
10 are automatically limited to that range.


2. HOW A TURN WORKS
===================

Each nation takes a turn. Within a nation's turn, its ships act one after
another.

The current ship is marked by an animated selection aura. Its information is
shown in the left-side HUD:

- ship type;
- movement points remaining;
- map coordinates;
- crew;
- attack strength;
- gold carried.

Move the current ship until its movement points are exhausted, or finish that
ship's turn manually. The game then activates the next ship. After the last
ship has finished, play passes to the next nation.

The pirate faction also receives turns and acts automatically.


3. KEYBOARD CONTROLS
====================

SHIP MOVEMENT ON THE HEX MAP
----------------------------

              U       I
               \     /
                \   /
          H ----- ship ----- K
                /   \
               /     \
              N       M

U  - move upper-left
I  - move upper-right
H  - move left
K  - move right
N  - move lower-left
M  - move lower-right

Movement is allowed only onto sea tiles. A ship cannot normally move through
land, mountains, coast tiles or another living ship.

COMBAT
------

Ctrl + movement key - attack an enemy ship in the selected adjacent hex.

Example:

Ctrl + K attacks an enemy immediately to the right.

Pressing a movement key without Ctrl when an enemy occupies the destination
will not attack. The game will ask you to confirm the attack by using Ctrl.

SHIP ACTIONS
------------

B  - collect an item from the current sea tile; costs 1 movement point
O  - print detailed information about the current ship and castle to the
     PowerShell or command window
J  - finish the current ship's turn
P  - open the home-port purchase screen

PORT KEYS
---------

1  - buy a Sloop for 1 gold
2  - buy a Brigantine for 2 gold
3  - buy a Frigate for 3 gold
0  - leave the port without buying a ship

The port screen also opens automatically when a ship reaches its own castle.
Gold used for purchases must already be deposited in the castle.

CAMERA AND GENERAL CONTROLS
---------------------------

Arrow keys       - move the camera around the map
Right mouse drag - drag the map
Numpad 0         - centre the camera on the current player's castle
Escape           - exit the game
D                - toggle developer/debug display mode

Numpad 5 is present in the current code as a camera-centre command, but it
references an unfinished player property and may cause an error. Avoid using
Numpad 5 until this function is repaired.

MOUSE CONTROLS
--------------

Left-click the orange "End Turn" button to finish the current ship's turn.

Left-clicking ships, castles, villages, map tiles and HUD objects currently
provides limited inspection or developer-console information. Clicking a ship
does not change which ship is active; ships are activated automatically in
turn order.


4. SHIP TYPES
=============

SLOOP
-----
Crew:          40
Movement:      16 points per turn
Attack:        10
Purchase cost: 1 gold

Best use:
Fast transport, village collection, scouting and low-cost replacement ships.

BRIGANTINE
----------
Crew:          50
Movement:      14 points per turn
Attack:        20
Purchase cost: 2 gold

Best use:
Balanced escort, transport and combat.

FRIGATE
-------
Crew:          60
Movement:      12 points per turn
Attack:        30
Purchase cost: 3 gold

Best use:
Heavy combat, protecting important routes and attacking enemy fleets.

English ships receive one additional movement point per turn.


5. WIND AND MOVEMENT COST
=========================

The compass and wind arrow show the current wind direction. Wind changes as
turns progress.

A movement deducts the following number of movement points:

- sailing directly with the wind:       1 point;
- one direction away from the wind:     2 points;
- two directions away from the wind:    3 points;
- sailing directly against the wind:    4 points.

Therefore, the same ship can travel much farther by following the wind.
Movement strength is currently displayed, but the present prototype mainly
uses wind direction to calculate cost.


6. GOLD ECONOMY
===============

Each nation owns two villages. To collect village gold:

1. Sail onto one of your own village hexes.
2. The ship automatically loads gold when the village is ready.
3. Return to your own castle.
4. Gold is automatically transferred from the ship to the castle.

Village collection has a cooldown. Remaining on or immediately returning to
the same village will not continuously generate gold.

The amount loaded per successful village visit depends on ship type:

- Sloop:       1 gold;
- Brigantine:  2 gold;
- Frigate:     3 gold.

A ship has a practical cargo limit controlled by the current prototype rules.
The current carried amount is displayed in the HUD as "Gold".

When a ship reaches its own castle:

- all carried gold is deposited;
- the crew is restored to maximum;
- normal attack strength is restored;
- the port purchase screen opens.

Only gold stored in the castle counts toward economic victory and can be used
to buy ships.


7. SEA ITEMS AND RANDOM EVENTS
==============================

Some sea tiles contain collectible items. Press B while standing on such a
tile. Collection costs 1 movement point and can cause one of several random
effects:

Possible negative effects:

- lose 10 crew;
- lose 1 carried gold;
- lose 10 attack for the next battle;
- lose 3 movement points during the current turn.

Possible positive effects:

- gain 10 attack for the next battle;
- gain 1 gold;
- gain 10 crew;
- gain 3 movement points during the current turn.

French ships receive an extra luck bonus and are less exposed to the worst
outcomes.


8. COMBAT
=========

To attack, hold Ctrl and press the movement key corresponding to an adjacent
enemy ship.

Combat is resolved by a random roll:

- on a successful attack, the defender loses crew equal to the attacker's
  attack value;
- on a failed attack, the attacker loses crew equal to the defender's attack
  value.

Base attack values are:

- Sloop:      10;
- Brigantine: 20;
- Frigate:    30.

A ship is destroyed when its crew reaches zero or below.

When an enemy ship is defeated, there is also a chance to capture it instead
of leaving only a wreck. Spanish attackers receive a higher capture chance.
A captured ship is added to the attacker's fleet, although captured-ship
recovery is still a prototype feature and may require returning it to port.

Pirates are hostile and may attack any nation. Pirate ships do not need to be
destroyed to satisfy the normal military victory condition.


9. NATIONAL ADVANTAGES
======================

ENGLISH
-------
Advantage: every English ship receives +1 movement point per turn.

Best suited to:

- rapid village collection;
- long transport routes;
- avoiding unfavourable battles;
- attacking exposed enemy couriers.

DUTCH
-----
Advantage: better odds when attacking. The normal successful-attack chance is
approximately 50%; the Dutch bonus increases it to approximately 55%.

Best suited to:

- offensive play;
- attacking first;
- concentrating Brigantines and Frigates against priority targets.

FRENCH
------
Advantage: +1 luck when collecting sea items. This removes the worst random
result and improves access to positive outcomes.

Best suited to:

- exploring item-rich areas;
- strengthening ships before battle;
- combining economic routes with item collection.

SPANISH
-------
Advantage: increased chance to capture a defeated enemy ship. The normal
capture chance is approximately 15%; the Spanish chance is approximately 20%.

Best suited to:

- fleet expansion through combat;
- targeting weakened enemy ships;
- converting naval victories into additional ships.


10. HOW TO WIN
==============

There are two victory conditions.

ECONOMIC VICTORY
----------------

Deposit at least the selected target amount of gold in your castle.

The target is selected on the start screen and can be between 3 and 10 gold.
Gold carried by ships does not count until it is delivered to the castle.

MILITARY VICTORY
----------------

Destroy all surviving ships belonging to the other English, Dutch, French and
Spanish nations.

Pirate ships are excluded from this victory calculation. You may win while
pirates are still present on the map.


11. PRACTICAL STRATEGIES
========================

STRATEGY A - FAST ECONOMIC VICTORY
----------------------------------

1. Use Sloops as dedicated gold couriers.
2. Choose the nearest or safest owned village.
3. Follow the wind rather than taking the shortest geometric route.
4. Return gold to the castle frequently instead of carrying a large load.
5. Avoid combat unless an enemy blocks the route.
6. Spend gold only when a replacement or escort is necessary.

This is usually strongest with England because of its movement bonus.

STRATEGY B - ESCORTED TRADE ROUTE
---------------------------------

1. Send a Sloop or Brigantine to collect gold.
2. Keep a Brigantine or Frigate near the route as an escort.
3. Use the escort to attack enemy raiders before they reach the courier.
4. Repair both ships by returning to the castle.
5. Bank gold before taking further risks.

This approach balances economic progress and fleet survival.

STRATEGY C - NAVAL DOMINATION
-----------------------------

1. Collect enough early gold to buy a Frigate.
2. Keep combat ships together instead of spreading them across the map.
3. Attack isolated ships and avoid fighting several enemies at once.
4. Prefer attacking a damaged or weaker ship.
5. Return damaged valuable ships to port for full crew restoration.
6. Eliminate one rival fleet at a time.

The Dutch attacking bonus makes this strategy more reliable.

STRATEGY D - CAPTURE FLEET
--------------------------

1. Play Spain.
2. Use Brigantines or Frigates to reduce enemy crew quickly.
3. Target ships carrying gold, because a captured ship can retain its load.
4. Protect captured ships and move them toward your port.
5. Build fleet size through captures rather than only through purchases.

Capture remains random, so keep enough gold for normal replacements.

STRATEGY E - ITEM EXPLORER
--------------------------

1. Play France.
2. Route ships through sea tiles containing items.
3. Collect items when the ship still has enough movement to react to a bad
   result.
4. Use attack bonuses before entering combat.
5. Bank any bonus gold rather than exposing it unnecessarily.

Items can accelerate progress, but they should supplement rather than replace
a reliable village route.


12. GENERAL TACTICAL ADVICE
===========================

- Watch the wind before every move. A longer-looking route may cost fewer
  movement points.
- Do not carry more gold than necessary. A destroyed ship can lose the value
  of an entire journey.
- Use Sloops for speed and Frigates for combat; Brigantines are the flexible
  middle option.
- Attack deliberately. Combat can damage the attacker even when the defender
  is weaker.
- A damaged ship is valuable if it can reach port, because crew repairs are
  free and complete.
- Protect your last ships. Losing every non-pirate ship gives an opponent a
  military victory even if your castle contains gold.
- Economic victory is often faster with a low gold target. Military victory
  becomes more practical in longer games with a higher target.
- The pirates are dangerous but are not part of the military victory count.
  Avoid wasting ships on pirates unless they threaten your route.
- Use the End Turn button or J when a ship has no useful action. Conserving
  time is better than making an unnecessary risky move.


13. WINDOWS QUICK START
=======================

Requirements:

- Windows 10 or Windows 11;
- Python 3.11 for development testing.

Open PowerShell in the project directory and run:

    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    .\run_game.ps1

If PowerShell blocks the script, run:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then run:

    .\run_game.ps1

To run the automated hex-grid tests:

    .\run_tests.ps1


14. CURRENT PROTOTYPE LIMITATIONS
=================================

- AI pathfinding still contains older square-grid assumptions and is planned
  for replacement with proper hex-grid pathfinding.
- Numpad 5 camera centring is not currently reliable.
- The minimap is mainly visual and does not yet provide navigation.
- Clicking ships does not manually select them.
- Some information is printed to the PowerShell window instead of appearing
  in the game interface.
- Save and load are not yet implemented.
- Captured-ship handling and replay behaviour still require further testing.
- Game balance, AI decisions and collision handling remain under development.

These limitations describe the current development build and are expected to
change as the project is improved.
