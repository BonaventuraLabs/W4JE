import pygame as pg
from src.player.player import Player
from src.hud.camera import Camera


class EventManager:
    def __init__(self, game):
        self.game = game

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()

            # dispatch all registered key
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()

                elif event.key == pg.K_d:
                    # debug mode
                    self.game.debug_mode = not self.game.debug_mode

                elif event.key in Player.keys_all:
                    # Player keys
                    self.game.player_turn_manager.current_player.handle_keys(event)

                elif event.key in Camera.keys_all:
                    # Camera keys
                    self.game.camera.handle_keys(event)

            # switch dragging on-off
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                self.game.mouse_drag = True
                self.game.mouse_drag_xy = pg.mouse.get_pos()

            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                self.game.mouse_drag = False

            # left click
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                click_xy_in_screen = pg.mouse.get_pos()
                # to convert screen coordinates to map coordinates, we need to apply camera shift.
                # shift the screen click coordinates by the Camera offset:
                shift_xy = self.game.camera.rect.topleft
                click_xy_in_map = [cl-sh for cl, sh in zip(click_xy_in_screen, shift_xy)]

                test_clicked_item = None

                # Test HUD. Test by SCREEN COORDINATES
                if test_clicked_item is None:
                    test_clicked_item = self.game.hud.get_clicked(click_xy_in_screen)

                # Test Unit Sprites (ship, castle, enemies?). Test by SCREEN COORDINATES
                # for now only players are checked.
                if test_clicked_item is None:
                    test_clicked_item = self.game.player_turn_manager.get_clicked(click_xy_in_map)

                # test map?  test by MAP COORDINATES
                if test_clicked_item is None:
                    test_clicked_item = self.game.map.get_clicked(click_xy_in_map)

                #print(test_clicked_item)



