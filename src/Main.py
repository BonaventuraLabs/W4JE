import sys
from collections import deque
import pygame as pg
from src.utilities.settings import *
from src.hud.hud import Hud
from src.hud.camera import Camera
from src.utilities.image_manager import ImageManager
from src.map.map import Map
from src.map.atmosphere import Atmosphere
from src.eventmanager.event_manager import EventManager
from src.player.player import Player
from src.player.turn_manager import TurnManager

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

        self.sprites_all = pg.sprite.Group()
        self.sprites_anim = pg.sprite.Group()
        self.sprites_unit = pg.sprite.Group()
        self.sprites_map = pg.sprite.Group()
        # self.sprites_hud = pg.sprite.Group()
        self.sprites_menu = pg.sprite.Group()

        self.event_manager = EventManager(self)
        self.map = Map(self)
        self.hud = Hud(self)
        self.atmosphere = Atmosphere(self)
        self.camera = Camera(self.map.width, self.map.height)

        # self.turn_manager = TurnManager(self)

        self.player_deque = deque([Player(self, 'Dimas', YELLOW),
                                  Player(self, 'Alex', RED),
                                  Player(self, 'Danila', GREEN)])

        self.current_player = self.player_deque[0]
        self.current_player.set_current()
        self.turn_finished = False

        self.mouse_drag = False
        self.mouse_drag_xy = self.current_player.ship.xy
        self.playing = True

    def run(self):
        while self.playing:
            # self.dt = self.clock.tick(FPS) / 1000
            # print(self.clock.tick(FPS))

            # dispatch events.
            self.event_manager.check_events()

            # update some events; for instance, camera shift, or menu.
            # self.update_some_events()

            # if finished, update state.
            if self.current_player.is_done:
                # self.current_player.update()
                self.update_state_on_turn()
                # go to next player
                self.player_deque.rotate(1)
                self.current_player = self.player_deque[0]
                self.current_player.set_current()

            # Do animations always
            self.update_animation()
            self.draw()

    def update_animation(self):
        self.sprites_anim.update()

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
        for sprite in self.sprites_unit:
            sprite.draw()
        self.atmosphere.draw()
        self.hud.draw()
        pg.display.flip()

    def update_state_on_turn(self):
        self.atmosphere.wind.get_new_direction()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def quit(self):
        pg.quit()
        sys.exit()


g = Game()
#g.show_start_screen()

while True:
    g.run()
    #g.show_go_screen()

g.quit()

