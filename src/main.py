import pygame as pg
from src.settings import *
import sys
from src.Utilities import ImageLoader, Hud
from src.MapUtilities import Map, Camera, Wind
from src.Units import Ship
from collections import deque

class Game:
    def __init__(self):
        # init and create window
        pg.init()
        pg.key.set_repeat(500, 50)
        self.font = pg.font.SysFont("comicsansms", 20)

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.images = ImageLoader(self)

        self.sprites_anim = pg.sprite.Group()
        self.unit_sprites = pg.sprite.Group()
        self.map_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.hud_layer_sprites = pg.sprite.Group()

        self.map = Map(self)
        self.wind = Wind(self)
        self.hud = Hud(self)
        self.camera = Camera(self.map.width, self.map.height)


        self.player_deque = deque([Ship(self, 10, 10, 'Dimas', YELLOW),
                                  Ship(self, 12, 12, 'Alex', RED),
                                  Ship(self, 15, 15, 'Danila', GREEN)
                                  ])
        self.current_player = self.player_deque[0]
        self.current_player.set_current()
        self.message = ''

        self.playing = True
        self.turn_finished = False

    def run(self):
        while self.playing:
            # self.dt = self.clock.tick(FPS) / 1000
            # Do animations continuously
            self.update_animation()

            self.draw()

            # check events, see if the turn is finished.
            self.events()

            # update some events; for instance, camera shift, or menu.
            # self.update_some_events()

            # if finished, update state.
            if self.current_player.is_done:
                #self.current_player.update()
                self.update_state_on_turn()
                # go to next player
                self.player_deque.rotate(1)
                self.current_player = self.player_deque[0]
                self.current_player.set_current()

    def update_animation(self):
        self.sprites_anim.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                else:
                    self.current_player.check_key_input()
                    self.camera.check_key_input()

    def update_state_on_turn(self):
        self.wind.get_new_direction()


    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.map_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.unit_sprites:
            sprite.draw()
        # for sprite in self.hud_layer_sprites:
        #     self.screen.blit(sprite.image, sprite)
        self.hud.draw()

        pg.display.flip()

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

