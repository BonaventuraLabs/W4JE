import sys
from collections import deque
import pygame as pg
from src.map.text import Text
from src.utilities.settings import *
from src.hud.hud import Hud
from src.hud.bottom_scroll import BottomHud
from src.hud.camera import Camera
from src.utilities.image_manager import ImageManager
from src.map.map import Map
from src.map.atmosphere import Atmosphere
from src.eventmanager.event_manager import EventManager
from src.player.player import Player
from src.player.player_turn_manager import PlayerTurnManager
from src.game_flow.start_screen import InputBox
from src.game_flow.button import Button

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from .context import sample

# TODO: where to keep instance images?
# If tiles have the same image, then we probably dont need to instantiate it for each tile.
# It will be waste of memory, since it's one same image. Instead, we should keep it as a static image of a class?
class Game:
    def __init__(self):
        # init and create window
        pg.init()
        pg.key.set_repeat(500, 50)
        self.font = pg.font.SysFont("comicsansms", 20)

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.image_manager = ImageManager(self)

        self.sprites_anim = pg.sprite.Group()
        self.sprites_unit = pg.sprite.Group()
        self.sprites_menu = pg.sprite.Group()

        self.event_manager = EventManager(self)
        self.map = Map(self)
        self.atmosphere = Atmosphere(self)
        self.hud = Hud(self)
        self.bottom_hud = BottomHud(self)
        self.camera = Camera(self)

        self.mouse_drag = False
        self.playing = True
        self.debug_mode = False
        self.pname1 = 'Computer'
        self.pname2 = 'Computer'
        self.pname3 = 'Computer'
        self.pname4 = 'Computer'
        self.gold_to_win = 7
        self.waiting = True
        self.starts = self.image_manager.starts
        self.rectp = self.starts.get_rect()

    def run(self):
        while self.playing:
            # self.dt = self.clock.tick(FPS) / 1000
            # print(self.clock.tick(FPS))

            # dispatch events.
            self.event_manager.check_events()

            # if finished, update state.
            self.player_turn_manager.check_state()

            # Do animations always
            self.update_animation()
            self.draw()

    def update_animation(self):
        self.map.animate()
        self.atmosphere.animate()
        for sprite in self.sprites_anim:
            sprite.update()

        #TODO: make a dragger class?
        if self.mouse_drag:
            xy = pg.mouse.get_pos()
            # print('-------')
            # print(xy)
            delta_x = self.mouse_drag_xy[0] - xy[0]
            delta_y = self.mouse_drag_xy[1] - xy[1]
            # print(delta_x)

            self.mouse_drag_xy = xy
            # print(self.mouse_drag_xy)
            self.camera.rect.x -= delta_x
            self.camera.rect.y -= delta_y
        else:
            # self.mouse_drag_xy
            pass

    def draw(self):
        self.screen.fill(BLACK)
        self.map.draw()
        if not self.debug_mode:
            for sprite in self.sprites_unit:
                sprite.draw()
        self.atmosphere.draw()
        self.hud.draw()
        self.bottom_hud.draw()
        pg.display.flip()

    def show_start_screen(self):
        text = Text(self)
        input_box1 = InputBox(50, 230, 140, 32, self.screen, 'Computer')
        input_box2 = InputBox(50, 310, 140, 32, self.screen, 'Computer')
        input_box3 = InputBox(50, 390, 140, 32, self.screen, 'Computer')
        input_box4 = InputBox(50, 470, 140, 32, self.screen, 'Computer')
        input_box5 = InputBox(50, 550, 40, 32, self.screen, '7')
        input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]
        start_button = Button(g, self.screen, 110, 640, 'Start Game')
        #pg.display.flip()
        self.waiting = True
        while self.waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                for box in input_boxes:
                    box.handle_event(event)
                start_button.handle_event(event)

            for box in input_boxes:
                box.update()

            #self.screen.fill((187, 200, 200))
            self.screen.blit(self.starts, self.rectp)
            text.draw_text("Welcome to War For Jenkin's Ear!", 50, 575, 55)
            text.draw_text("Enter player name by the nation", 40, 560, 150)
            text.draw_text("English: +1 move", 24, 370, 230)
            text.draw_text("Dutch: when attacking extra battle win chance", 24, 538, 310)
            text.draw_text("French: extra luck", 24, 385, 390)
            text.draw_text("Spanish: extra chance to capture enemy ship", 24, 525, 470)
            text.draw_text("Enter amount of gold to win (from 3 to 10)", 24, 520, 550)
            for box in input_boxes:
                box.draw(self.screen)
            start_button.draw()
            pg.display.flip()
        self.pname1 = input_box1.txt
        self.pname2 = input_box2.txt
        self.pname3 = input_box3.txt
        self.pname4 = input_box4.txt
        tm = int(input_box5.txt)
        if tm < 3:
            tm = 3
        elif tm > 10:
            tm = 10
        self.gold_to_win = tm
        self.start()


    def start(self):
        self.player_turn_manager = PlayerTurnManager(self)
        self.mouse_drag_xy = self.player_turn_manager.current_player.castle.xy
        self.run_game()

    def show_end_screen(self, player_name, player_nation):
        player = player_name
        nation = player_nation
        text = Text(self)
        input_box = InputBox(50, 150, 140, 32, self.screen, 'Y')
        end_button = Button(g, self.screen, 110, 300, 'Continue')
        self.waiting = True

        while self.waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                input_box.handle_event(event)
                end_button.handle_event(event)

            input_box.update()

            self.screen.fill((187, 200, 200))
            text.draw_text("Player " + player + ' ' + nation + " won the game!", 40, 575, 55)
            text.draw_text("Do you wish to play again? Y or N", 24, 450, 150)
            input_box.draw(self.screen)
            end_button.draw()

            pg.display.flip()
        if input_box.txt == 'Y':
            for pl in self.player_turn_manager.player_deque:
                pl.is_done = True
                pl.is_current = False
                for sh in pl.ships:
                    sh.destroyed = True
                    sh.is_current = False
                    sh.is_done = True

            for pl in self.player_turn_manager.player_deque:
                pl.ships.clear()
                if pl.color != BLACK:
                    pl.villages.clear()
            self.player_turn_manager.player_deque.clear()
            pg.display.flip()
            g.show_start_screen()
        else:
            g.quit()

    def win_check(self, player):
        pl = player
        if pl.castle.gold >= self.gold_to_win:
            g.show_end_screen(pl.name, pl.nation)
        count_enemy_ships = 0
        for plr in g.player_turn_manager.player_deque:
            for sh in plr.ships:
                if not sh.destroyed:
                    if plr != pl:
                        if plr.color != BLACK:
                            count_enemy_ships += 1
        #print('Alive enemy ships for ' + pl.name + ' ' + str(count_enemy_ships))
        if count_enemy_ships == 0:
            g.show_end_screen(pl.name, pl.nation)


    def show_go_screen(self):
        pass

    def quit(self):
        pg.quit()
        sys.exit()

    def run_game(self):
        while True:
            g.run()

g = Game()
g.show_start_screen()

g.quit()

