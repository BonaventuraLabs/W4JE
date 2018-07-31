from src.utilities.settings import *
import pygame as pg


class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.speed = CAMERA_SPEED

    # def apply(self, target):
    #     return target.rect.move(self.camera.topleft)

    def apply(self, target):
        if hasattr(target, 'rect'):
            rect = target.rect
        elif hasattr(target, 'get_rect'):
            rect = target.get_rect()
        elif isinstance(target, pg.Rect):
            rect = target
        return rect.move(self.rect.topleft)

    def update(self, x, y):
        # def update(self, target):
        #     x = -target.rect.x + int(WIDTH/2)
        #     y = -target.rect.y + int(HEIGHT/2)
        #     self.camera = pg.Rect(x, y, self.width, self.height)

        # same as old, but directly with x and y; this is more flexible than "target.rect.x"
        x_shifted = - x + int(WIDTH / 2)
        y_shifted = - y + int(HEIGHT / 2)
        self.rect = pg.Rect(x_shifted, y_shifted, self.width, self.height)

    def move_left(self):
        self.rect.x += self.speed

    def move_right(self):
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y += self.speed

    def move_down(self):
        self.rect.y -= self.speed
