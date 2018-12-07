from src.utilities.settings import *
import sys


class ButtonStart:

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.image = pg.Surface((120, 40))
        self.image.fill((150, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 700)
        self.id = 'start_button'

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

        text = 'Start Game'
        label = self.game.font.render(text, True, BLACK)
        label_rect = label.get_rect()
        label_rect.center = self.rect.center
        self.game.screen.blit(label, label_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the button

            if self.rect.collidepoint(event.pos):
                self.game.waiting = False
                print('Clicked')






