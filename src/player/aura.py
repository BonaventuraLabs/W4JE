from src.utilities.settings import *
import pygame as pg


class Aura(pg.sprite.Sprite):
    def __init__(self, owner):
        self.groups = owner.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.owner = owner
        self.image = self.generate_image()
        # proper position:
        self.rect = self.image.get_rect()

        self.image_fixed = self.image.copy()
        self.rect_fixed = self.rect.copy()

        self.phase_speed = 0.001
        self.phase_min = 0.75
        self.phase_max = 1
        self.phase = self.phase_max
        self.phase_change = -self.phase_speed


    def generate_image(self):
        # square surface, 2*tile:
        w = 2 * TILEWIDTH
        sel_surf = pg.Surface((w, w), pg.SRCALPHA, 32).convert_alpha()
        sel_surf.set_alpha(128)

        # draw circle in the center of this surface:
        center = (int(TILEWIDTH), int(TILEWIDTH))
        r1 = int(TILEWIDTH * 0.75)
        r2 = int(TILEWIDTH * 0.95)
        thickness = 3
        color = self.owner.player.color#LIGHTGREY
        pg.draw.circle(sel_surf, color, center, r1, 0)
        pg.draw.circle(sel_surf, color, center, r2, thickness)
        return sel_surf

    def set_center(self, xy):
        self.rect.center = xy

    def update(self):
        # oscillating (triangle oscillator) of the phase between phase_min and max:
        if self.phase >= self.phase_max:
            self.phase_change = -self.phase_speed
        if self.phase <= self.phase_min:
            self.phase_change = +self.phase_speed
        self.phase += self.phase_change
        new_w = int(self.rect_fixed.w * self.phase)
        new_h = int(self.rect_fixed.h * self.phase)
        self.image = pg.transform.scale(self.image_fixed, (new_w, new_h))
        self.rect = self.image.get_rect()
        self.rect.center = self.owner.xy

