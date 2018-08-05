import pygame as pg
from src.player.ship import Ship
from src.utilities.settings import *
import numpy as np
from src.player.battle import Battle


class Pirate:

    def __init__(self, game, name, color):
        self.game = game
        self.color = color
        self.name = name

        # position at generation:
        # shuffle available tiles:
        np.random.shuffle(self.game.map.spawn_tiles_list)
        row, col = self.game.map.spawn_tiles_list.pop()

        self.ship = PirateShip(game, self, row, col)

        # turn parameters
        # self.turn_finished = False
        # not his turn at creation:
        self.is_current = False
        self.is_done = True

    def handle_move(self):
        self.ship.handle_move()


class PirateShip(pg.sprite.Sprite):
    def __init__(self, game, player, row, col):
        self.game = game
        self.player = player
        self.groups = self.game.sprites_unit, self.game.sprites_anim

        super().__init__(self.groups)
        #pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.image_manager.pirate_ship
        self.rect = self.image.get_rect()

        # tile coordinates:
        self.r = row
        self.c = col
        self.r_prev = self.r
        self.c_prev = self.c

        # xy coordinates
        self.xy = None
        self.recalc_center()
        self.xy_prev = self.xy[:]

        self.rect.center = self.xy

        self.moves_per_turn = SHEEP_SPEED  # equivalent of speed
        self.moves_left = self.moves_per_turn
        self.move_penalty = 0  # nothing yet.

        self.moving_anim_on = False

        self.hp = 50
        self.attack = 10
        self.defense = 10
        self.destroyed = False

        self.chance_to_change_dir = 10  # percents,
        self.chosen_direction = np.random.choice(['l', 'lu', 'ru', 'r', 'rd', 'ld'])

    def get_another_direction(self):
        if np.random.randint(0, 100) < self.chance_to_change_dir:
            self.chosen_direction = np.random.choice(['l', 'lu', 'ru', 'r', 'rd', 'ld'])

    def recalc_center(self):
        # save the old values:
        self.r_prev = self.r
        self.c_prev = self.c
        self.xy_prev = self.xy

        # recalculate
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))
        label, label_rect = self.get_name_label()
        self.game.screen.blit(label, self.game.camera.apply(label_rect))

    def get_name_label(self):
        text = self.player.name + '. Moves: ' + self.chosen_direction
        label = self.game.font.render(text, True, WHITE)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        label_rect.bottom = self.rect.bottom
        return label, label_rect

    def handle_move(self):
        if self.destroyed:
            return
        # print('Pirate move')
        self.get_another_direction()
        self.analyze_move(self.chosen_direction)

    def analyze_move(self, cur_move):
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

        # get the desired r, c
        target_r, target_c = self.calculate_target_rc(cur_move)

        # see, if there is a ship or castle or enemy in the target tile:
        target_unit = None
        for p in self.game.player_turn_manager.player_deque:
            if (p.ship.r, p.ship.c) == (target_r, target_c):
                target_unit = p.ship
            # if (p.castle.r, p.castle.c) == (target_r, target_c):
            #     target_units.append(p.castle)

        if target_unit is not None:
            if mov_forced:
                self.moves_left = 0
                battle = Battle(self, target_unit)
                battle.start()
                return
            else:
                print('\nIf you really want to attack, press (Ctrl+KeyPad)')
                print('After battle finishes, you will have no moves left.')
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

        self.r = target_r
        self.c = target_c
        self.recalc_center()

        # this part is for animation.
        # set animation ON
        self.moving_anim_on = True
        # we have to start from OLD r,c:
        self.rect.center = self.xy_prev  # self.xy

    def make_destroyed(self):
        self.destroyed = True
        self.moves_left = 0
        self.moves_per_turn = 0
        self.image = self.game.image_manager.ship_wreck

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
