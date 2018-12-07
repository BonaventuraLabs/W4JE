from src.utilities.settings import *
from src.player.explosion import Explosion
from src.player.battle import Battle
from src.player.aura import Aura
import random
import pygame as pg
import numpy as np

values = {'Sloop': 1, 'Brigantine': 2, 'Frigate': 3}

class AIship(pg.sprite.Sprite):
    def __init__(self, game, player, row, col, rank):
        self.game = game
        self.player = player
        self.ships_nation = player.nation
        self.rank = rank
        if self.rank == 'Sloop':
            self.max_crew = 40
            self.moves_per_turn = 16
            self.image = self.game.image_manager.sloop
        elif self.rank == 'Brigantine':
            self.max_crew = 50
            self.moves_per_turn = 14
            self.image = self.game.image_manager.brigantine
        else:
            self.max_crew = 60
            self.moves_per_turn = 12
            self.image = self.game.image_manager.frigate
        self.crew = self.max_crew
        self.captured = False
        self.ships_nation = player.nation
        # English get longer move perk
        if self.ships_nation == 'English':
            self.moves_per_turn += 1
        self.status = ''
        self.groups = self.game.sprites_unit, self.game.sprites_anim

        super().__init__(self.groups)

        self.rect = self.image.get_rect()

        # tile coordinates:
        self.r = row
        self.c = col
        self.r_prev = self.r
        self.c_prev = self.c
        self.next_loc = (0, 0)

        # xy coordinates
        self.xy = None
        self.recalc_center()
        self.xy_prev = self.xy[:]

        self.rect.center = self.xy

        #self.moves_per_turn = SHEEP_SPEED  # equivalent of speed
        self.moves_left = self.moves_per_turn
        self.move_penalty = 0  # nothing yet.
        self.load = 0
        self.aura = Aura(self)
        self.moving_anim_on = False

        self.attack = values.get(self.rank) * 10
        self.destroyed = False

        self.chance_to_change_dir = 10  # percents,
        self.chosen_direction = np.random.choice(['l', 'lu', 'ru', 'r', 'rd', 'ld'])
        self.is_done = True
        self.is_current = False
        self.moving_left = True

    #def get_another_direction(self):
    #    if np.random.randint(0, 100) < self.chance_to_change_dir:
    #        self.chosen_direction = np.random.choice(['l', 'lu', 'ru', 'r', 'rd', 'ld'])
    #    self.get_direction()

    def get_direction(self):
        my_map = self.game.map.tiles
        start = (self.r, self.c)
        if self.load == 0 and self.crew > 0:
            end = (self.player.villages[0].r, self.player.villages[0].c)
        else:
            end = (self.player.castle.r, self.player.castle.c)
        #print(start)
        #print(end)
        path = self.astar(my_map, start, end)
        #print('Next step should be: ' + str(path[1]))

        #Check if touches a fish
        cur_tile = self.game.map.tiles_dict['%s.%s' % (path[1][0], path[1][1])]
        #cur_tile.inspect_tile()
        # collect item
        item = cur_tile.remove_one_item()
        if item:
            self.game.map.add_fish()
            luck = random.randint(1, 8)
            print('Luck = ', luck)
            if self.ships_nation == 'French':
                luck += 1
                print('French extra luck player luck = ', luck)
            if luck == 1:
                self.crew -= 10
                print('Your crew decreased by 10.')
            if luck == 2:
                if self.load > 0:
                    self.load -= 1
                    print('You lost 1 gold')
                else:
                    print('You could have lost 1 gold, but had nothing')
            if luck == 3:
                if self.attack > 0:
                    self.attack -= 10
                    print('Your attack decreased by 10 for one strike.')
            if luck == 4:
                if self.moves_left > 0:
                    self.moves_left -= 3
                    print('Your sailing path decreased by 3 for 1 turn!')
            if luck == 5:
                self.attack += 10
                print('Your attack increased by 10 for one strike!')
            if luck == 6:
                self.moves_left += 3
                print('Your sailing path increased by 3 for 1 turn.')
            if luck == 7:
                self.crew += 10
                print('Your crew increased by 10!')
            if luck > 7:
                self.load += 1
                print('You got 1 gold!')


        # Check if touches a village
        if self.player.villages[0].r == path[1][0] and self.player.villages[0].c == path[1][1]:
            self.load += values.get(self.rank)
        #  Check if touches own Castle
        if self.player.castle.r == path[1][0] and self.player.castle.c == path[1][1]:
            self.player.castle.gold += self.load
            self.game.win_check(self.player)
            self.load = 0
            self.crew = self.max_crew
            self.attack = values.get(self.rank) * 10

        if path[1][0] == self.c + 1 and path[1][1] == self.r:
            self.chosen_direction = 'r'
        elif path[1][0] == self.c - 1 and path[1][1] == self.r:
            self.chosen_direction = 'l'
        elif self.r % 2 == 0:
            if path[1][0] == self.c - 1 and path[1][1] == self.r + 1:
                self.chosen_direction = 'ld'
            elif path[1][0] == self.c and path[1][1] == self.r + 1:
                self.chosen_direction = 'rd'
            elif path[1][0] == self.c - 1 and path[1][1] == self.r - 1:
                self.chosen_direction = 'lu'
            elif path[1][0] == self.c and path[1][1] == self.r - 1:
                self.chosen_direction = 'ru'
        elif self.r % 2 != 0:
            if path[1][0] == self.c and path[1][1] == self.r + 1:
                self.chosen_direction = 'ld'
            elif path[1][0] == self.c + 1 and path[1][1] == self.r + 1:
                self.chosen_direction = 'rd'
            elif path[1][0] == self.c + 1 and path[1][1] == self.r - 1:
                self.chosen_direction = 'ru'

        self.next_loc = path[1]

    def recalc_center(self):
        # save the old values:
        self.r_prev = self.r
        self.c_prev = self.c
        self.xy_prev = self.xy

        # recalculate
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy

    def get_bar(self):
        w = 2 * TILEWIDTH
        bar = pg.Surface((w, w), pg.SRCALPHA, 32).convert_alpha()
        pct = self.crew / self.max_crew
        fill = pct * TILEWIDTH
        outline_rect = pg.Rect(int(TILEWIDTH), int(TILEWIDTH), TILEWIDTH, 7)
        fill_rect = pg.Rect(int(TILEWIDTH), int(TILEWIDTH), fill, 7)
        pg.draw.rect(bar, self.player.color, fill_rect)
        pg.draw.rect(bar, WHITE, outline_rect, 1)
        bar_rect = bar.get_rect()
        bar_rect.centerx = self.rect.centerx - 24
        bar_rect.centery = self.rect.centery + 38
        #bar_rect.bottom = self.rect.bottom + 60
        return bar, bar_rect

    def draw(self):
        if not self.destroyed:
            if self.is_current:
                self.game.screen.blit(self.aura.image, self.game.camera.apply(self.aura))
            label, label_rect = self.get_name_label()
            self.game.screen.blit(label, self.game.camera.apply(label_rect))
            bar, bar_rect = self.get_bar()
            self.game.screen.blit(bar, self.game.camera.apply(bar_rect))
            self.game.screen.blit(self.image, self.game.camera.apply(self))
        else:
            self.moves_left = 0
            self.moves_per_turn = 0
            self.is_done = True
            self.is_current = False

    def get_name_label(self):
        text = self.ships_nation
        label = self.game.font.render(text, True, WHITE)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        label_rect.bottom = self.rect.bottom + 35
        return label, label_rect

    def handle_keys(self, event):
        pass

    def handle_move(self):
        if self.destroyed:
            return
        #self.get_another_direction()
        #self.analyze_move(self.chosen_direction)
        self.get_direction()
        self.analyze_move(self.next_loc, self.chosen_direction)

    def analyze_move(self, next_loc, cur_move):
        # get wind penalty:
        self.move_penalty = self.game.atmosphere.wind.ship_movement_penalty_dict[cur_move]

        # movement is forced:
        mov_forced = True

        # No wind: I maximize the move penalty as to have only 1 movement per turn.
        if self.game.atmosphere.wind.current_strength == 0:
            if mov_forced:
                self.move_penalty = -self.moves_per_turn
            else:
                pass
        # Undelete THIS
        # get the desired r, c
        #target_r, target_c = self.calculate_target_rc(cur_move)
        target_r = next_loc[0]
        target_c = next_loc[1]

        # see, if there is a ship or castle or enemy in the target tile:
        target_unit = None
        if self.ships_nation in ('Dutch', 'Spanish'):
            # Look around of your current location for enemy ships
            if self.crew > 0:
                for p in self.game.player_turn_manager.player_deque:
                    for sh in p.ships:
                        if (sh.r, sh.c) == (self.r+1, self.c):
                            target_unit = p.get_ship_by_xy(self.r+1, self.c)
                        if (sh.r, sh.c) == (self.r+1, self.c+1):
                            target_unit = p.get_ship_by_xy(self.r+1, self.c+1)
                        if (sh.r, sh.c) == (self.r+1, self.c-1):
                            target_unit = p.get_ship_by_xy(self.r+1, self.c-1)
                        if (sh.r, sh.c) == (self.r-1, self.c):
                            target_unit = p.get_ship_by_xy(self.r-1, self.c)
                        if (sh.r, sh.c) == (self.r-1, self.c+1):
                            target_unit = p.get_ship_by_xy(self.r-1, self.c+1)
                        if (sh.r, sh.c) == (self.r-1, self.c-1):
                            target_unit = p.get_ship_by_xy(self.r-1, self.c-1)
                        if (sh.r, sh.c) == (self.r, self.c):
                            target_unit = p.get_ship_by_xy(self.r, self.c)
                        if (sh.r, sh.c) == (self.r, self.c+1):
                            target_unit = p.get_ship_by_xy(self.r, self.c+1)
                        if (sh.r, sh.c) == (self.r, self.c-1):
                            target_unit = p.get_ship_by_xy(self.r, self.c-1)

        if target_unit is not None:
            if target_unit.player != self.player and not target_unit.destroyed:
                self.moves_left = 0
                battle = Battle(self, target_unit)
                battle.start()
                self.attack = values.get(self.rank) * 10
                # take a chance to capture target ship
                if target_unit.destroyed:
                    if target_unit.captured:
                        self.status = 'Juppiiiii! Enemy ship is captured!'
                        print('Juppiiiii!' + self.ships_nation + 'captured enemy ship!')
                        captured_ship = AIship(self.game, self.player, target_r, target_c, target_unit.rank)
                        captured_ship.crew = 0
                        captured_ship.load = target_unit.load
                        self.player.ships.append(captured_ship)
                return


        if self.destroyed:
            print('Ship is dead.')
            return

        # If survived: see, if target tile is allowed (if sea)
        target_tile = self.game.map.get_tile_by_rc(target_r, target_c)
        # print('targeted tile: ' + target_tile.__str__())

        if target_tile is None:
            return
        elif target_tile.type != 'sea':
            return
        elif target_tile.type == 'sea':
            pass

        # estimate if move is possible:
        if (self.moves_left + self.move_penalty) < 0:
            pass

        self.make_move(target_r, target_c)

    def make_move(self, target_r, target_c):
        # apply penalty
        self.moves_left += self.move_penalty
        #self.game.map.tiles[self.r, self.c] = 0
        #if target_r != self.player.villages[0].r and target_c != self.player.villages[0].c:
        #    self.game.map.tiles[target_r, target_c] = 9
        self.r = target_r
        self.c = target_c
        self.recalc_center()
        #print(self.game.map.tiles)
        # this part is for animation.
        # set animation ON
        self.moving_anim_on = True
        # we have to start from OLD r,c:
        self.rect.center = self.xy_prev  # self.xy


    def make_destroyed(self):
        self.moves_left = 0
        self.moves_per_turn = 0
        if not self.captured:
            self.game.sprites_anim.add(Explosion(self.game, self.xy, self.rank))
            self.image = self.game.image_manager.ship_wreck
        self.destroyed = True
        self.is_done = True
        self.is_current = False

    def on_click(self):
        print('Click : ' + self.player.name + ' ship')

    def calculate_target_rc(self, cur_move):
        """
        This function translates phenomenological description into coordinates.
        This is needed because of the complex grid structure.
        :param cur_move: movement descriptor 'lu' - left-up, 'rd' - right-down and so on.
        :return: None
        """
        if cur_move == 'ld':
            # left-down, ld.
            if self.r % 2 == 0:
                r = self.r + 1
                c = self.c - 1
            else:
                r = self.r + 1
                c = self.c
        elif cur_move == 'rd':
            # right-down, rd
            if self.r % 2 == 0:
                r = self.r + 1
                c = self.c
            else:
                r = self.r + 1
                c = self.c + 1
        elif cur_move == 'l':
            # left, l
            r = self.r
            c = self.c - 1
        elif cur_move == 'r':
            # right, r
            r = self.r
            c = self.c + 1
        elif cur_move == 'lu':
            # left up, lu
            if self.r % 2 == 0:
                r = self.r - 1
                c = self.c - 1
            else:
                r = self.r - 1
                c = self.c
        elif cur_move == 'ru':
            # rightup, ru
            if self.r % 2 == 0:
                r = self.r - 1
                c = self.c
            else:
                r = self.r - 1
                c = self.c + 1
        return r, c

    def update(self, *args):
        if self.moving_anim_on:
            # check in which direction should move:
            dx = self.xy[0] - self.rect.center[0]
            dy = self.xy[1] - self.rect.center[1]

            if dx > 0:
                self.rect.center = (
                self.rect.center[0] + 1, self.rect.center[1])  # stupid, because tuple cannot be += 1
            if dx < 0:
                self.rect.center = (self.rect.center[0] - 1, self.rect.center[1])
            if dy > 0:
                self.rect.center = (self.rect.center[0], self.rect.center[1] + 1)
            if dy < 0:
                self.rect.center = (self.rect.center[0], self.rect.center[1] - 1)

            # check if done
            if abs(dx) < 1 and abs(dy) < 1:
                self.moving_anim_on = False
                self.rect.center = self.xy

    def astar(self, maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given map"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
