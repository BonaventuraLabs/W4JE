import pygame as pg
from src.settings import *
import sys
from src.Utilities import ImageLoader
from src.MapUtilities import Map, Camera


class Game:
    def __init__(self):
        # init and create window
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(1000, 100)
        self.clock = pg.time.Clock()
        self.images = ImageLoader(self)
        self.unit_sprites = pg.sprite.Group()
        self.map_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        #TODO: the ship is added inside Map(). We need to decouple it from Map()
        self.ship = None
        self.map = Map(self)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        # self.turn_finished = False
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # Do animations continuously
            # but movement of units - only on EndTurn!
            self.events()
            # if self.turn_finished:
            self.update()
                # self.turn_finished = False

            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                # if event.key == pg.K_e:
                #     self.turn_finished = True

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.ship)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.map_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.unit_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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

