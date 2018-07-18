import pygame as pg
from settings import *

pg.init()


# initialize the pygame module
pg.init()

# load and set the logo
screen = pg.display.set_mode((240, 180))
pg.display.set_caption("W4JE")

# create a surface on screen that has the size of 240 x 180

# define a variable to control the main loop
running = True

# main loop
while running:
    # event handling, gets all event from the eventqueue
    for event in pg.event.get():
        # only do something if the event is of type QUIT
        if event.type == pg.QUIT:
            # change the value to False, to exit the main loop
            running = False


pg.quit()
