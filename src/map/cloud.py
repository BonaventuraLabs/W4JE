import numpy as np
import pygame as pg


class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = np.random.choice(self.game.image_manager.cloud_list)
        self.rect = self.image.get_rect()
        self.rect.center = (np.random.randint(0, self.game.map.width),
                            np.random.randint(0, self.game.map.height))
        self.frame_skipper = 0
        self.frame_skipper_max = 10

    def update(self, *args):
        # make it slower!!!.
        if self.frame_skipper < self.frame_skipper_max:
            self.frame_skipper += 1
            return
        else:
            self.frame_skipper = 0

        angle = self.game.atmosphere.wind.current_angle
        strength = self.game.atmosphere.wind.current_strength
        self.rect.x += strength * np.cos(np.deg2rad(90 + angle))
        self.rect.y -= strength * np.sin(np.deg2rad(90 + angle))

        if self.rect.left > self.game.map.width:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.game.map.width
        if self.rect.top > self.game.map.height:
            self.rect.bottom = 0
        if self.rect.bottom > self.game.map.height:
            self.rect.top = self.game.map.height

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))
