from engine_render_DDA import *
import pygame
import math

player_pos = (3, 2)
player_angle = 0
player_speed = 0.004
player_rot_speed = 0.002

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = player_pos
        self.angle = player_angle

    def movement(self):
        keys = pygame.key.get_pressed()
        speed = player_speed * self.game.delta_time
        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dx += math.cos(self.angle) * speed
            dy += math.sin(self.angle) * speed
        if keys[pygame.K_s]:
            dx -= math.cos(self.angle) * speed
            dy -= math.sin(self.angle) * speed
        if keys[pygame.K_a]:
            dx += math.sin(self.angle) * speed
            dy -= math.cos(self.angle) * speed
        if keys[pygame.K_d]:
            dx -= math.sin(self.angle) * speed
            dy += math.cos(self.angle) * speed

        self.rotate(dx, dy)

    def rotate(self, dx, dy):
        self.angle -= player_rot_speed * self.game.delta_time * (pygame.key.get_pressed()[pygame.K_LEFT] - pygame.key.get_pressed()[pygame.K_RIGHT])
        self.angle %= math.tau

        scale = 100 / self.game.delta_time
        if self.wall_collision(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.wall_collision(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def wall_collision(self, x, y):
        return (x, y) not in self.game.map.world_map

    def draw(self):
        pygame.draw.circle(self.game.screen, 'green', (int(self.x * player_scale), int(self.y * player_scale)), 6)

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
