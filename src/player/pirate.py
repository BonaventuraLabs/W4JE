from src.utilities.settings import *
import numpy as np
from src.player.battle import Battle

class Pirate:

    def __init__(self, game, name, color, rw, cl, nation):
        self.game = game
        self.color = color
        self.name = name
        self.nation = nation
        # position at generation:
        # shuffle available tiles: TEMPORARY DISABLED
        #np.random.shuffle(self.game.map.spawn_tiles_list)
        #row, col = self.game.map.spawn_tiles_list.pop()
        row, col = [rw, cl]

        self.ships = []
        self.ships.append(PirateShip(game, self, row, col, 'Sloop'))
        #self.ship = PirateShip(game, self, row, col, 'Sloop')

        # turn parameters
        # self.turn_finished = False
        # not his turn at creation:
        self.is_current = False
        self.is_done = True
        self.show_port = False

    def handle_move(self):
        self.ships[0].handle_move()

    def get_ship_by_xy(self, x, y):
        for s in self.ships:
            if s.r == x:
                if s.c == y:
                    return s


class PirateShip(pg.sprite.Sprite):
    def __init__(self, game, player, row, col, rank):
        self.game = game
        self.player = player
        self.ships_nation = player.nation
        self.rank = rank
        if self.rank == 'Sloop':
            self.max_crew = 40
            self.moves_per_turn = 12
        elif self.rank == 'Brigantine':
            self.max_crew = 50
            self.moves_per_turn = 10
        else:
            self.max_crew = 60
            self.moves_per_turn = 8
        if self.ships_nation == 'English':
            self.moves_per_turn += 1
        self.crew = self.max_crew
        self.status = ''
        self.groups = self.game.sprites_unit, self.game.sprites_anim

        super().__init__(self.groups)
        #pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.image_manager.pirate_ship
        self.rect = self.image.get_rect()
        self.captured = False

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

        #self.moves_per_turn = SHEEP_SPEED  # equivalent of speed
        self.moves_left = self.moves_per_turn
        self.move_penalty = 0  # nothing yet.

        self.moving_anim_on = False

        self.load = 0
        self.attack = 10
        self.defense = 10
        self.destroyed = False

        self.chance_to_change_dir = 10  # percents,
        self.chosen_direction = np.random.choice(['l', 'lu', 'ru', 'r', 'rd', 'ld'])
        self.is_done = True
        self.is_current = False

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
        if not self.destroyed:
            #if self.is_current:
            #    self.game.screen.blit(self.aura.image, self.game.camera.apply(self.aura))
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
        #bar_rect.x = self.xy[0] - 82
        #bar_rect.y = self.xy[1] - 20
        bar_rect.centerx = self.rect.centerx - 24
        bar_rect.centery = self.rect.centery + 38
        #bar_rect.bottom = self.rect.bottom + 60
        return bar, bar_rect


#    def draw(self):
#        if self.destroyed:
#            self.moves_left = 0
#            self.moves_per_turn = 0
#            self.is_done = True
#            self.is_current = False
#        self.game.screen.blit(self.image, self.game.camera.apply(self))
#        label, label_rect = self.get_name_label()
#        self.game.screen.blit(label, self.game.camera.apply(label_rect))

    def get_name_label(self):
        text = self.player.name
        label = self.game.font.render(text, True, WHITE)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        label_rect.bottom = self.rect.bottom + 35
        return label, label_rect

    def handle_move(self):
        if self.destroyed:
            return
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
            for sh in p.ships:
                if (sh.r, sh.c) == (self.r + 1, self.c):
                    target_unit = p.get_ship_by_xy(self.r + 1, self.c)
                if (sh.r, sh.c) == (self.r + 1, self.c + 1):
                    target_unit = p.get_ship_by_xy(self.r + 1, self.c + 1)
                if (sh.r, sh.c) == (self.r + 1, self.c - 1):
                    target_unit = p.get_ship_by_xy(self.r + 1, self.c - 1)
                if (sh.r, sh.c) == (self.r - 1, self.c):
                    target_unit = p.get_ship_by_xy(self.r - 1, self.c)
                if (sh.r, sh.c) == (self.r - 1, self.c + 1):
                    target_unit = p.get_ship_by_xy(self.r - 1, self.c + 1)
                if (sh.r, sh.c) == (self.r - 1, self.c - 1):
                    target_unit = p.get_ship_by_xy(self.r - 1, self.c - 1)
                if (sh.r, sh.c) == (self.r, self.c):
                    target_unit = p.get_ship_by_xy(self.r, self.c)
                if (sh.r, sh.c) == (self.r, self.c + 1):
                    target_unit = p.get_ship_by_xy(self.r, self.c + 1)
                if (sh.r, sh.c) == (self.r, self.c - 1):
                    target_unit = p.get_ship_by_xy(self.r, self.c - 1)

        if target_unit is not None:
            if target_unit.player != self.player and not target_unit.destroyed:
                if mov_forced:
                    self.moves_left = 0
                    battle = Battle(self, target_unit)
                    battle.start()
                    return
                else:
                    print('If you really want to attack, press (Ctrl+KeyPad)')
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


