
from src.utilities.settings import *



class InputBox:

    def __init__(self, x, y, w, h, screen, tx):
        self.screen = screen
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color(COLOR_INACTIVE)
        self.txt = tx
        self.txt_surface = FONT.render(self.txt, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.

            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.txt = ''
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pg.Color(COLOR_ACTIVE) if self.active else pg.Color(COLOR_INACTIVE)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.txt)
                    self.txt = ''
                elif event.key == pg.K_BACKSPACE:
                    self.txt = self.txt[:-1]
                else:
                    self.txt += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.txt, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



