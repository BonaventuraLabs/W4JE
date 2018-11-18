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
        # self.game.screen.blit(self.port, self.rectp)
        input_box1 = InputBox(50, 150, 140, 32, self.screen)
        input_box2 = InputBox(50, 230, 140, 32, self.screen)
        input_box3 = InputBox(50, 310, 140, 32, self.screen)
        input_box4 = InputBox(50, 390, 140, 32, self.screen)
        input_boxes = [input_box1, input_box2, input_box3, input_box4]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            self.screen.fill((187, 200, 200))
            text.draw_text("Enter player name by the nation", 40, 575, 55)
            text.draw_text("English: +1 move", 24, 370, 150)
            text.draw_text("Dutch: when attacking extra battle win chance", 24, 550, 230)
            text.draw_text("French: extra luck", 24, 385, 310)
            text.draw_text("Spanish: extra chance to capture enemy ship", 24, 530, 390)
            for box in input_boxes:
                box.draw(self.screen)

            pg.display.flip()
            #self.clock.tick(30)

        self.pname1 = input_box1.txt
        print(self.pname1)
        self.pname2 = input_box2.txt
        print(self.pname2)
        self.pname3 = input_box3.txt
        print(self.pname3)
        self.pname4 = input_box4.txt
        print(self.pname4)
        self.player_turn_manager = PlayerTurnManager(self)
        self.mouse_drag_xy = self.player_turn_manager.current_player.castle.xy

    def show_go_screen(self):
        pass

    def quit(self):
        pg.quit()
        sys.exit()


g = Game()
g.show_start_screen()



while True:
    g.run()

g.quit()

