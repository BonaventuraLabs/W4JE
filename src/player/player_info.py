import pygame as pg
from src.utilities.settings import *


class PlayerInfo:
    def __init__(self, game, hud):
        self.game = game
        self.image = pg.Surface((120, 60))
        self.image.fill((150, 120, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 310)

    def draw(self):

        # blit box:
        self.game.screen.blit(self.image, self.rect)

        # blit player info:
        cur_player = self.game.player_turn_manager.current_player
        cur_color = BLACK #cur_player.color

        info_str = '%s. moves: %s / %s '%(cur_player.name, cur_player.ship.moves_left, cur_player.ship.moves_per_turn)
        label = self.game.font.render(info_str, True, cur_color)
        label_rect = label.get_rect(center=(100, HEIGHT / 2))
        self.game.screen.blit(label, label_rect)

        text = 'Coordinates: ' + str(cur_player.ship.r) + '-' + str(cur_player.ship.c)
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect(center=(100, HEIGHT / 2 + 20))
        self.game.screen.blit(label, label_rect)

    @staticmethod
    def blit_text(surface, text, pos, font, color=pg.Color('black')):
        """Blit words in a multi-line format
        source: https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
        """
        WORD_WIDTH = surface.width
        WORD_HEIGHT = surface.height

        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

