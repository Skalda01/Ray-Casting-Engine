from engine_render_DDA import *
import pygame as pg

_ = False
mini_map = [
    [1]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value


    def draw(self):
        for pos in self.world_map:
            pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * player_scale, pos[1] * player_scale, player_scale, player_scale), 1)