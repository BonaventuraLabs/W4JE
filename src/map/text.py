import pygame as pg
from src.utilities.settings import *


class Text:

    def __init__(self, game):
        self.game = game

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(pg.font.match_font("comicsansms"), size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.game.screen.blit(text_surface, text_rect)