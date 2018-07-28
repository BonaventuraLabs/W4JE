import pygame as pg


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
                # Unit movement
                elif event.key in [pg.K_KP1, pg.K_KP3, pg.K_KP4, pg.K_KP6, pg.K_KP7, pg.K_KP9]:
                    self.game.current_player.ship.move(event.key)
                # center camera on player
                elif event.key == pg.K_KP5:
                    self.game.camera.update(self.game.current_player.ship.rect.x,
                                            self.game.current_player.ship.rect.y)

                # Camera:
                elif event.key == pg.K_LEFT:
                    self.game.camera.move_left()
                elif event.key == pg.K_RIGHT:
                    self.game.camera.move_right()
                elif event.key == pg.K_UP:
                    self.game.camera.move_up()
                elif event.key == pg.K_DOWN:
                    self.game.camera.move_down()

            # switch dragging on-off
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.game.mouse_drag = True
                self.game.mouse_drag_xy = pg.mouse.get_pos()

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.mouse_drag = False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                print('--- testing rmb ----')
                m_pos = [a-b for a,b in zip(pg.mouse.get_pos(), self.game.camera.rect.topleft)]
                m_pos_corr = m_pos # correct by camera shift!
                for k, tile in self.game.map.tiles_dict.items():
                    if tile.rect.collidepoint(m_pos_corr):
                        print(tile)

