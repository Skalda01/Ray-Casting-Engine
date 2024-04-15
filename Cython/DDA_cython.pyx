
import pygame
import math
import time
from menu_settings import *


half_width = WIDTH / 2
half_height = HEIGHT / 2
fov = math.pi / 3
half_fov = fov / 2
ray_array = WIDTH //2
half_num_rays = ray_array // 2
delta_angle = fov / ray_array
max_depth = 100
screen_distance = half_width / math.tan(half_fov)
scale = WIDTH // ray_array
texture_size = 256
half_texture_size = texture_size / 2
player_scale = 20


class RayCastingDDA:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = {i: pygame.transform.scale(pygame.image.load(f'texture/{i}.png').convert_alpha(),
                                                        (texture_size, texture_size)) for i in range(1, 6)}
        self.objects_to_render = []
        self.textures = self.wall_textures

    def update_ray_casting(self):
        self.objects_to_render = []
        ox, oy = self.game.player.pos
        ray_angle = self.game.player.angle - half_fov

        for ray in range(ray_array):

            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)
            map_x, map_y, step_x, step_y, side_dist_x, side_dist_y, delta_dist_x, delta_dist_y = self.init_dda_variables(
                ox, oy, sin_a, cos_a)
            side, map_x, map_y = self.perform_dda(map_x, map_y, step_x, step_y, side_dist_x, side_dist_y, delta_dist_x,
                                                  delta_dist_y)
            depth = self.calculate_depth(ox, oy, map_x, map_y, step_x, step_y, side, cos_a, sin_a)
            proj_height, wall_column, wall_pos = self.calculate_wall_projection(depth, side, ox, oy, sin_a, cos_a, ray,
                                                                                map_x, map_y)

            self.objects_to_render.append((depth, wall_column, wall_pos))
            self.draw_ray(ox, oy, depth, cos_a, sin_a)
            ray_angle += delta_angle



    def init_dda_variables(self, ox, oy, sin_a, cos_a):
        map_x, map_y = int(ox), int(oy)
        delta_dist_x, delta_dist_y = abs(1 / cos_a), abs(1 / sin_a)
        step_x = 1 if cos_a >= 0 else -1
        step_y = 1 if sin_a >= 0 else -1
        if cos_a >= 0:
            side_dist_x = (map_x + 1.0 - ox) * delta_dist_x
        else:
            side_dist_x = (ox - map_x) * delta_dist_x
        if sin_a >= 0:
            side_dist_y = (map_y + 1.0 - oy) * delta_dist_y
        else:
            side_dist_y = (oy - map_y) * delta_dist_y
        return map_x, map_y, step_x, step_y, side_dist_x, side_dist_y, delta_dist_x, delta_dist_y

    def perform_dda(self, map_x, map_y, step_x, step_y, side_dist_x, side_dist_y, delta_dist_x, delta_dist_y):
        hit = False
        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            if (map_x, map_y) in self.game.map.world_map:
                hit = True
        return side, map_x, map_y

    def calculate_depth(self, ox, oy, map_x, map_y, step_x, step_y, side, cos_a, sin_a):
        if side == 0:
            depth = (map_x - ox + (1 - step_x) / 2) / cos_a
        else:
            depth = (map_y - oy + (1 - step_y) / 2) / sin_a
        return depth

    def calculate_wall_projection(self, depth, side, ox, oy, sin_a, cos_a, ray, map_x, map_y):
        texture = self.game.map.world_map[(map_x, map_y)]
        if side == 0:
            offset = oy + depth * sin_a
        else:
            offset = ox + depth * cos_a
        offset %= 1
        proj_height = screen_distance / (depth + 0.0001)
        wall_column, wall_pos = self.render_wall_column(texture, offset, proj_height, ray)
        return proj_height, wall_column, wall_pos

    def render_wall_column(self, texture, offset, proj_height, ray):
        if proj_height < HEIGHT:
            wall_column = self.textures[texture].subsurface(offset * (texture_size - scale), 0, scale, texture_size)
            wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
            wall_pos = (ray * scale, half_height - proj_height // 2)
        else:
            texture_height = texture_size * HEIGHT / proj_height
            wall_column = self.textures[texture].subsurface(
                offset * (texture_size - scale),
                half_texture_size - texture_height // 2, scale, texture_height
            )
            wall_column = pygame.transform.scale(wall_column, (scale, HEIGHT))
            wall_pos = (ray * scale, 0)

        return wall_column, wall_pos

    def draw(self):
        self.render_engine_object()

    def render_engine_object(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def draw_ray(self, ox, oy, depth, cos_a, sin_a):
        pygame.draw.line(self.game.screen, 'red', (player_scale * ox, player_scale * oy),
                         (player_scale * ox + player_scale * depth * cos_a, player_scale * oy + player_scale * depth * sin_a), 1)

