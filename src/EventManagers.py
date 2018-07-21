import pygame as pg


class KeyManager:
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

                # Unit movement
                elif event.key == pg.K_KP1:
                    self.game.current_player.move_ld()
                elif event.key == pg.K_KP3:
                    self.game.current_player.move_rd()
                elif event.key == pg.K_KP4:
                    self.game.current_player.move_l()
                elif event.key == pg.K_KP6:
                    self.game.current_player.move_r()
                elif event.key == pg.K_KP7:
                    self.game.current_player.move_lu()
                elif event.key == pg.K_KP9:
                    self.game.current_player.move_ru()

                # Camera:
                elif event.key == pg.K_LEFT:
                    self.camera.move_left()
                elif event.key == pg.K_RIGHT:
                    self.camera.move_right()
                elif event.key == pg.K_UP:
                    self.camera.move_up()
                elif event.key == pg.K_DOWN:
                    self.camera.move_down()

            # switch dragging on-off
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                self.game.rmb_drag = True
                self.game.rmb_dag_xy = pg.mouse.get_pos()

            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                self.game.rmb_drag = False

