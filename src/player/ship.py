import numpy as np
from src.utilities.settings import *
from src.player.aura import Aura
from src.player.battle import Battle
import pygame as pg

values = {'Sloop': 1, 'Brigantine': 2, 'Frigate': 3}

class Ship(pg.sprite.Sprite):

    keys_ship_move = [pg.K_t, pg.K_y, pg.K_h, pg.K_b, pg.K_v, pg.K_f]
    keys_ship_collect = [pg.K_c]
    keys_inspect = [pg.K_i]
    keys_end_turn = [pg.K_g]

    keys_all = keys_ship_move + keys_end_turn + keys_ship_collect + keys_inspect

    def __init__(self, game, player, row, col, rank):
        self.game = game
        self.player = player
        self.rank = rank
        self.load = 0
        if self.rank == 'Sloop':
            self.crew = 30
            self.moves_per_turn = 12
            self.image = self.game.image_manager.sloop
        elif self.rank == 'Brigantine':
            self.crew = 40
            self.moves_per_turn = 10
            self.image = self.game.image_manager.brigantine
        else:
            self.crew = 50
            self.moves_per_turn = 8
            self.image = self.game.image_manager.frigate
        self.groups = self.game.sprites_unit, self.game.sprites_anim

        #pg.sprite.Sprite.__init__(self, self.groups)
        super().__init__(self.groups)


        self.aura = Aura(self)
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

        self.moves_left = self.moves_per_turn
        self.move_penalty = 0  # nothing yet.

        self.moving_anim_on = False

        self.hp = 100
        self.attack = values.get(self.rank) * 10
        self.destroyed = False

        self.items = []
        self.is_done = True
        self.is_current = False

    def handle_keys(self, event):
        if event.key in Ship.keys_ship_move:
            self.analyze_move(event)

        if event.key in Ship.keys_ship_collect:
            self.handle_collect(event)

        if event.key in Ship.keys_inspect:
            print('\nPlayer: ' + self.player.name)
            self.print_full_info()
            self.player.castle.print_full_info()

        if event.key == pg.K_g:
            self.is_done = True
            self.is_current = False
            self.moves_left = 0

    def draw(self):
        if self.is_current:
            self.game.screen.blit(self.aura.image, self.game.camera.apply(self.aura))
            if self.destroyed:
                self.moves_left = 0
                self.moves_per_turn = 0
                self.is_done = True
                self.is_current = False
        self.game.screen.blit(self.image, self.game.camera.apply(self))
        label, label_rect = self.get_name_label()
        self.game.screen.blit(label, self.game.camera.apply(label_rect))

    def get_name_label(self):
        text = self.player.name
        label = self.game.font.render(text, True, WHITE)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        label_rect.bottom = self.rect.bottom
        return label, label_rect

    def update(self, *args):

        if self.moving_anim_on:

            # check in which direction should move:
            dx = self.xy[0] - self.rect.center[0]
            dy = self.xy[1] - self.rect.center[1]

            if dx > 0:
                self.rect.center = (self.rect.center[0]+1, self.rect.center[1])  # stupid, because tuple cannot be += 1
            if dx < 0:
                self.rect.center = (self.rect.center[0] - 1, self.rect.center[1])
            if dy > 0:
                self.rect.center = (self.rect.center[0], self.rect.center[1] + 1)
            if dy < 0:
                self.rect.center = (self.rect.center[0], self.rect.center[1] - 1)

            self.aura.set_center(self.rect.center)

            # check if done
            if abs(dx) < 1 and abs(dy) < 1:
                self.moving_anim_on = False
                self.rect.center = self.xy
                self.aura.set_center(self.xy)
                # self.player.unset_current()

       # self.recalc_center()


        # shuffle aura
        if self.is_current:
            self.aura.update()
            self.game.camera.update(self.rect.x, self.rect.y)

    def recalc_center(self):
        # save the old values:
        self.r_prev = self.r
        self.c_prev = self.c
        self.xy_prev = self.xy

        # recalculate
        self.xy = self.game.map.rc_to_xy(self.r, self.c)
        self.rect.center = self.xy
        self.aura.set_center(self.xy)

    # -------------------------- Movement Functions --------------------------------
    def analyze_move(self, event):
        if self.destroyed:
            print('\n' + self.player.name + ': Ship is destroyed.')
            return

        # check if there are moves left:
        if self.moves_left <= 0:
            print('\n' + self.player.name + ': ship is out of moves.')
            return

        # movement direction:
        move_dir_dict = {pg.K_v: 'ld', pg.K_b: 'rd', pg.K_f: 'l',
                         pg.K_h: 'r', pg.K_t: 'lu', pg.K_y: 'ru'}
        cur_move = move_dir_dict[event.key]

        # get wind penalty:
        self.move_penalty = self.game.atmosphere.wind.ship_movement_penalty_dict[cur_move]
        # print(self.move_penalty)

        # check if the movement is forced:
        mov_forced = False
        if pg.key.get_mods() & pg.KMOD_SHIFT:
            pass
            # mov_forced = True
        if pg.key.get_mods() & pg.KMOD_CTRL:
            mov_forced = True

        # No wind: I maximize the move penalty as to have only 1 movement per turn.
        if self.game.atmosphere.wind.current_strength == 0:
            if mov_forced:
                self.move_penalty = -self.moves_per_turn
            else:
                print('\nNo wind...')
                print('You can spend your actions on something else, or move for 1 tile only (Ctrl+KeyPad).')
                return

        # get the desired r, c
        target_r, target_c = self.calculate_target_rc(cur_move)

        # see, if there is a ship or castle or enemy in the target tile:
        target_unit = None
        for p in self.game.player_turn_manager.player_deque:
            for sh in p.ships:
                if (sh.r, sh.c) == (target_r, target_c):
                    if not p.get_ship_by_xy(target_r, target_c).destroyed:
                        target_unit = p.get_ship_by_xy(target_r, target_c)
            # if (p.castle.r, p.castle.c) == (target_r, target_c):
            #     target_units.append(p.castle)

        if target_unit is not None:
            if mov_forced:
                #self.moves_left = 0 # no need to stop the shooting ship
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
            print('Tile does not exist.')
            return
        elif target_tile.type != 'sea':
            print('Tile is not sea!')
            return
        elif target_tile.type == 'sea':
            # movement allowed
            pass

        # estimate if move is possible:
        if (self.moves_left + self.move_penalty) < 0:
            print('Move is too demanding. You can spend your moves on something else.')
            return

        self.make_move(target_r, target_c)

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
        self.aura.set_center(self.rect.center)
        if self.moves_left <= 0:
            print('\n' + self.player.name + ': ship is out of moves.')
            self.is_done = True
            self.is_current = False

    def handle_collect(self, event):
        # check if enough moves are left:
        if self.moves_left <= 0:
            print('\n' + self.player.name + ': ship is out of moves.')
            self.is_done = True
            self.is_current = False
            return
        else:
            cur_tile = self.game.map.tiles_dict['%s.%s' % (self.r, self.c)]
            cur_tile.inspect_tile()
            self.moves_left -= 1

            # collect item
            item = cur_tile.remove_one_item()
            if item:
                self.items.append(item)

    def on_click(self):
        print('Click : ' + self.player.name + ' ship')

    def make_destroyed(self):
        self.moves_left = 0
        self.moves_per_turn = 0
        self.image = self.game.image_manager.ship_wreck
        self.destroyed = True
        self.is_done = True
        self.is_current = False


    def print_full_info(self):
        print('---=== SHIP ===---')
        print('Rank: ' + str(self.rank))
        print('Crew: ' + str(self.crew))
        print('Attack: ' + str(self.attack))
        print('Items:')
        if len(self.items) > 0:
            for item in self.items:
                print('  ' + item.name)
        else:
            print('None')