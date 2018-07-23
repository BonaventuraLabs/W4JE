import sys
from collections import deque
import pygame as pg
from src.Settings import *
from src.Hud import Hud, Camera
from src.Utilities import ImageManager
from src.MapUtilities import Map, Wind, Cloud, Seagull
from src.Units import Ship
from src.EventManagers import EventManager


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
        self.sprites_hud = pg.sprite.Group()

        self.event_manager = EventManager(self)
        self.map = Map(self)
        self.wind = Wind(self)
        self.hud = Hud(self)
        self.camera = Camera(self.map.width, self.map.height)
        self.clouds = []
        for i in range(0, CLOUD_COUNT):
            self.clouds.append(Cloud(self))
        self.seagulls = []
        for i in range(0, SEAGULL_COUNT):
            self.seagulls.append(Seagull(self))

        self.player_deque = deque([Ship(self, 10, 10, 'Dimas', YELLOW),
                                  Ship(self, 12, 12, 'Alex', RED),
                                  Ship(self, 15, 15, 'Danila', GREEN)])

        self.current_player = self.player_deque[0]
        self.current_player.set_current()

        self.playing = True
        self.turn_finished = False

        self.rmb_drag = False  # Right mouse button
        self.rmb_dag_xy = self.current_player.xy

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

        if self.rmb_drag:
            xy = pg.mouse.get_pos()
            # print('-------')
            # print(xy)
            delta_x = self.rmb_dag_xy[0] - xy[0]
            delta_y = self.rmb_dag_xy[1] - xy[1]
            # print(delta_x)

            self.rmb_dag_xy = xy
            # print(self.rmb_dag_xy)
            self.camera.rect.x -= delta_x
            self.camera.rect.y -= delta_y
        else:
            # self.rmb_dag_xy
            pass

    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.sprites_map:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.sprites_unit:
            sprite.draw()
        for seagull in self.seagulls:
            seagull.draw()
        for cloud in self.clouds:
            cloud.draw()
        # for sprite in self.sprites_hud:
        #     self.screen.blit(sprite.image, sprite)
        self.hud.draw()
        pg.display.flip()

    def update_state_on_turn(self):
        self.wind.get_new_direction()

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

