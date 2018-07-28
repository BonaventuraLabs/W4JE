import pygame as pg
from src.map.seagull import Seagull
from src.map.cloud import Cloud
from src.utilities.settings import *
from src.map.wind import Wind


class Atmosphere:
    def __init__(self, game):
        self.game = game
        self.wind = Wind(game)
        self.clouds = []
        for i in range(0, CLOUD_COUNT):
            self.clouds.append(Cloud(self.game))
        self.seagulls = []
        for i in range(0, SEAGULL_COUNT):
            self.seagulls.append(Seagull(self.game))

    def draw(self):
        for seagull in self.seagulls:
            seagull.draw()
        for cloud in self.clouds:
            cloud.draw()
