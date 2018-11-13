from src.utilities.settings import *
import pygame as pg


class Camera:

    keys_all = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_KP5, pg.K_KP0]

    def __init__(self, game):
        self.game = game
        self.rect = pg.Rect(0, 0, self.game.map.width_in_pix, self.game.map.height_in_pix)
        self.width = self.rect.w #.rectwidth
        self.height = self.rect.h #height
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
        x_shifted = min(0, x_shifted)
        x_shifted = max(-(self.width - WIDTH - TILEWIDTH), x_shifted)
        y_shifted = min(0, y_shifted)
        y_shifted = max(-(self.height - HEIGHT - TILEHEIGHT), y_shifted)
        self.rect = pg.Rect(x_shifted, y_shifted, self.width, self.height)

    def handle_keys(self, event):
        # move camera
        if event.key == pg.K_LEFT:
            self.move_left()
        elif event.key == pg.K_RIGHT:
            self.move_right()
        elif event.key == pg.K_UP:
            self.move_up()
        elif event.key == pg.K_DOWN:
            self.move_down()

        # center camera on current  player ship/castle
        elif event.key == pg.K_KP5:
            self.update(self.game.player_turn_manager.current_player.ship.rect.center[0],
                        self.game.player_turn_manager.current_player.ship.rect.center[1])
        elif event.key == pg.K_KP0:
            self.update(self.game.player_turn_manager.current_player.castle.rect.center[0],
                        self.game.player_turn_manager.current_player.castle.rect.center[1])


    def move_left(self):
        if self.rect.x + self.speed < 0:
            self.rect.x += self.speed

    def move_right(self):
        if self.rect.x > -(self.width - WIDTH - TILEWIDTH):
            self.rect.x -= self.speed

    def move_up(self):
        if self.rect.y + self.speed < 0:
            self.rect.y += self.speed

    def move_down(self):
        if self.rect.y > -(self.height - HEIGHT - TILEHEIGHT):
            self.rect.y -= self.speed


