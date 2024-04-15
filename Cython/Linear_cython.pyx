import math
import time
import pygame
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


class RayCastingLinear:
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
        angle = self.game.player.angle - half_fov + 0.0001

        for ray in range(ray_array):
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)

            depth, texture, offset = self.cast_ray(ox, oy, angle)
            depth *= math.cos(self.game.player.angle - angle)
            proj_height = screen_distance / (depth + 0.0001)

            wall_column, wall_pos = self.render_wall_column(depth, texture, offset, proj_height, ray)

            self.objects_to_render.append((depth, wall_column, wall_pos))
            self.draw_ray(ox, oy, depth, cos_a, sin_a)

            angle += delta_angle

    def cast_ray(self, ox, oy, ray_angle):
        depth_hor, texture_hor = self.cast_horizontal_ray(ox, oy, ray_angle)
        depth_vert, texture_vert = self.cast_vertical_ray(ox, oy, ray_angle)

        if depth_vert < depth_hor:
            depth, texture = depth_vert, texture_vert
            y_vert = oy + depth_vert * math.sin(ray_angle)
            offset = y_vert % 1 if math.cos(ray_angle) > 0 else 1 - (y_vert % 1)
        else:
            depth, texture = depth_hor, texture_hor
            x_hor = ox + depth_hor * math.cos(ray_angle)
            offset = x_hor % 1 if math.sin(ray_angle) > 0 else 1 - (x_hor % 1)

        return depth, texture, offset

    def cast_horizontal_ray(self, ox, oy, ray_angle):
        y_hor, dy = (self.game.player.map_pos[1] + 1, 1) if math.sin(ray_angle) > 0 else (
            self.game.player.map_pos[1] - 1e-6, -1)
        depth_hor = (y_hor - oy) / math.sin(ray_angle)
        x_hor = ox + depth_hor * math.cos(ray_angle)
        delta_depth = dy / math.sin(ray_angle)

        for _ in range(max_depth):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in self.game.map.world_map:
                return depth_hor, self.game.map.world_map[tile_hor]
            x_hor += delta_depth * math.cos(ray_angle)
            y_hor += dy
            depth_hor += delta_depth
        return max_depth, 1

    def cast_vertical_ray(self, ox, oy, ray_angle):
        x_vert, dx = (self.game.player.map_pos[0] + 1, 1) if math.cos(ray_angle) > 0 else (
            self.game.player.map_pos[0] - 1e-6, -1)
        depth_vert = (x_vert - ox) / math.cos(ray_angle)
        y_vert = oy + depth_vert * math.sin(ray_angle)
        delta_depth = dx / math.cos(ray_angle)

        for _ in range(max_depth):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in self.game.map.world_map:
                return depth_vert, self.game.map.world_map[tile_vert]
            x_vert += dx
            y_vert += delta_depth * math.sin(ray_angle)
            depth_vert += delta_depth
        return max_depth, 1



    def render_wall_column(self, depth, texture, offset, proj_height, ray):
        if proj_height < HEIGHT:
            wall_column = self.textures[texture].subsurface(offset * (texture_size - scale), 0, scale, texture_size)
            wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
            wall_pos = (ray * scale, half_height - proj_height // 2)
        else:
            texture_height = texture_size * HEIGHT / proj_height
            wall_column = self.textures[texture].subsurface(
                offset * (texture_size - scale), half_texture_size - texture_height // 2,
                scale, texture_height
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
                         (player_scale * ox + player_scale * depth * cos_a,
                          player_scale * oy + player_scale * depth * sin_a), 1)
