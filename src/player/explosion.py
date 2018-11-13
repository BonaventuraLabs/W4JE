import pygame as pg


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center, rank):
        self.game = game
        self.groups = self.game.sprites_unit, self.game.sprites_anim
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rank = rank
        self.image = self.game.image_manager.exp_list[self.rank][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 200
        #self.rect.center = self.owner.xy

    def update(self, *args):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.image_manager.exp_list[self.rank]):
                self.kill()
            else:
                center = self.rect.center
                #pg.time.wait(500)
                self.image = self.game.image_manager.exp_list[self.rank][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))