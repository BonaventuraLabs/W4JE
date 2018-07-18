import pygame as pg
from src.settings import *

print('Hello World!')

pg.init()

# initialize the pygame module
pg.init()

# create a surface on screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)


# define a variable to control the main loop
running = True

# main loop
while running:
    # event handling, gets all event from the event queue
    for event in pg.event.get():
        # only do something if the event is of type QUIT
        if event.type == pg.QUIT:
            # change the value to False, to exit the main loop
            running = False


pg.quit()
