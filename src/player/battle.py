import random


class Battle:
    def __init__(self, attacking_ship, defending_ship):
        self.a_ship = attacking_ship
        self.d_ship = defending_ship

    def calculate_damage(self):

        v1 = self.a_ship.attack
        v2 = self.d_ship.attack

        x = random.randint(1, 20)
        print('random = ' + str(x))
        if self.a_ship.ships_nation == 'Dutch':
            x -= 1
            print('Dutch random ' + str(x))
        if x > 10:  # attacking ship lost
                self.a_ship.crew -= v2
                self.a_ship.status = 'Watch out! You got minus ' + str(v2)
                print('Attacker ' + self.a_ship.ships_nation + ' random ' + str(x))
        else:
            self.d_ship.crew -= v1
            self.a_ship.status = 'Great shot! Defender minus ' + str(v1)
        if self.a_ship.crew <= 0:
            self.a_ship.make_destroyed()
        if self.d_ship.crew <= 0:
            c = random.randint(1, 20)
            print('Random should be more than 17 to capture. Random is ' + str(c))
            if self.a_ship.ships_nation == 'Spanish':
                c += 1
                print('Spanish c: ' + str(c))
            if c > 17:
                self.d_ship.captured = True
            self.d_ship.make_destroyed()

    def start(self):
        self.calculate_damage()

