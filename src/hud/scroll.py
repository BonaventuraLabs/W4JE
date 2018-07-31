import pygame as pg


class Scroll(pg.sprite.Sprite):

    def __init__(self, game, hud):
        self.game = game
        self.groups = hud.sprites_hud
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((WIDTH, HUD_HEIGHT))
        # self.image.fill((250, 250, 180))
        self.image = self.game.image_manager.hud_scroll
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
