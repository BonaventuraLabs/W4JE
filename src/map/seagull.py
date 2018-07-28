import numpy as np
import pygame as pg


class Seagull(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.image_manager.seagull
        self.rect = self.image.get_rect()

        self.frame_skipper = 0
        self.frame_skipper_max = 2

        self.orbit_r = np.random.randint(0, 200)
        self.orbit_c = (np.random.randint(0, self.game.map.width),
                        np.random.randint(0, self.game.map.height))
        self.orbit_angle = 0#np.random.randint(0, 360)
        self.orientation_angle = 0  # seagull looks upwards: --^--
        # self.rect.center
        self.recalculate_position()

    def recalculate_position(self):
        # angle = self.game.wind.current_angle
        cur_pos = (self.orbit_c[0] + self.orbit_r * np.cos(np.deg2rad(self.orbit_angle)),
                       self.orbit_c[1] + self.orbit_r * np.sin(np.deg2rad(self.orbit_angle)))
        self.rect.center = cur_pos

    def update(self, *args):
        # make it slower!!!.
        if self.frame_skipper < self.frame_skipper_max:
            self.frame_skipper += 1
            return
        else:
            self.frame_skipper = 0

        self.orientation_angle += 1
        self.orbit_angle -= 1
        self.recalculate_position()

        self.image = pg.transform.rotate(self.game.image_manager.seagull, self.orientation_angle)
        #self.rect = self.image.get_rect()


    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))
