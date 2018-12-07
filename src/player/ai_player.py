from src.player.ai_ship import AIship
from src.player.castle import Castle
from src.player.village import Village


class AI_Player:

    def __init__(self, game, name, color, rw, cl, nation):
        self.game = game
        self.color = color
        self.name = name
        self.nation = nation
        self.row = rw
        self.col = cl

        self.castle = Castle(game, self, self.row, self.col)
        if self.row == 4:
            vr1 = 45
            vc1 = 10
            vr2 = 46
            vc2 = 34
        elif self.row == 25 and self.col == 4:
            vr1 = 14
            vc1 = 42
            vr2 = 36
            vc2 = 42
        elif self.row == 25 and self.col == 45:
            vr1 = 38
            vc1 = 7
            vr2 = 14
            vc2 = 5
        else:
            vr1 = 5
            vc1 = 11
            vr2 = 3
            vc2 = 36

        self.villages = []
        self.villages.append(Village(game, self, vr1, vc1))
        self.villages.append(Village(game, self, vr2, vc2))
        self.ships = []
        self.ships.append(AIship(game, self, self.row, self.col, 'Sloop'))
        self.ships.append(AIship(game, self, self.row, self.col, 'Sloop'))
        self.ships.append(AIship(game, self, self.row, self.col, 'Brigantine'))

        self.is_current = False
        self.is_done = True
        self.show_port = False

    def handle_move(self):
        self.game.player_turn_manager.current_ship.handle_move()

    def get_ship_by_xy(self, x, y):
        for s in self.ships:
            if s.r == x:
                if s.c == y:
                    return s
