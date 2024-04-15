import pygame
import sys
import os
import engine_map
from engine_map import Map
from engine_player import Player
from engine_render_DDA import RayCastingDDA
from engine_render_Linear import RayCastingLinear
from menu_settings import *

# Import pro cython
# import DDA_cython
# import Linear_cython

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Res)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.current_algorithm = "Linear"  
        self.current_map = None  
        self.new_scene()
        self.memory_for_update = 0

    def new_scene(self):
        self.map = Map(self)
        self.player = Player(self)
        self.set_raycasting_algorithm() 

    def set_raycasting_algorithm(self):
        if self.current_algorithm == "Linear":
            # self.raycasting = Linear_cython.RayCastingLinear(self) CYTHON 
            self.raycasting = RayCastingLinear(self) # PYTHON
        elif self.current_algorithm == "DDA":
            # self.raycasting = DDA_cython.RayCastingDDA(self) CYTHON 
            self.raycasting = RayCastingDDA(self) # PYTHON


    def draw_engine(self):
        self.screen.fill((0, 0, 0))
        self.raycasting.draw()
        self.map.draw()
        self.player.draw()

    def update_engine(self):
        self.player.update()
        self.raycasting.update_ray_casting()
        pygame.display.flip()
        self.delta_time = self.clock.tick(60)

    def close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def display_menu(self):
        font_title = pygame.font.SysFont(None, 75)
        font_info = pygame.font.SysFont(None, 50)
        font_options = pygame.font.SysFont(None, 45)

        text_title_rendered = font_title.render("Ray Casting engine", True, (255, 255, 255))
        text_info_rendered = font_info.render("Vyberte algoritmus", True, (255, 255, 255))
        text_linear_rendered = font_options.render("Linear algoritmus", True, (255, 255, 255))
        text_dda_rendered = font_options.render("DDA algoritmus", True, (255, 255, 255))

        text_title_pos = text_title_rendered.get_rect(center=(WIDTH / 2, 100))
        text_info_pos = text_info_rendered.get_rect(center=(WIDTH / 2, 180))
        text_linear_pos = text_linear_rendered.get_rect(center=(WIDTH / 2, 350))
        text_dda_pos = text_dda_rendered.get_rect(center=(WIDTH / 2, 450))

        self.screen.blit(text_title_rendered, text_title_pos)
        self.screen.blit(text_info_rendered, text_info_pos)
        self.screen.blit(text_linear_rendered, text_linear_pos)
        self.screen.blit(text_dda_rendered, text_dda_pos)

        if text_linear_pos.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255, 0, 0), text_linear_pos.inflate(10, 10),2) 
        if text_dda_pos.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255, 0, 0), text_dda_pos.inflate(10, 10),2)  
       

    def display_texture_menu(self):
        texture_paths = self.get_texture_paths()
        if not texture_paths:
            return

        texture_height = 150
        total_width = len(texture_paths) * (texture_height + 10) 
        start_x = (WIDTH - total_width) / 2 

        menu_rect = pygame.Rect(start_x - 20, 800 - 20, total_width + 25, 230)
        pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 2)  

        font = pygame.font.SysFont("None", 45)
        text_title_rendered = font.render("Použité textury", True, (255, 255, 255))
        text_title_pos = text_title_rendered.get_rect(midtop=(menu_rect.centerx-295, menu_rect.top - 60))
        self.screen.blit(text_title_rendered, text_title_pos)

        for i, path in enumerate(texture_paths):
            texture = pygame.image.load(path)
            texture = pygame.transform.scale(texture, (texture_height, texture_height))
            texture_rect = texture.get_rect(topleft=(start_x + i * (texture_height + 10), 800))
            self.screen.blit(texture, texture_rect)

            font = pygame.font.SysFont(None, 36)
            file_name = os.path.basename(path)  
            file_name_with_extension = os.path.splitext(file_name)[0] + ".png"  
            text_rendered = font.render(file_name_with_extension, True, (255, 255, 255))
            text_rect = text_rendered.get_rect(midtop=(texture_rect.centerx, texture_rect.bottom + 20))
            self.screen.blit(text_rendered, text_rect)

    def select_map(self):
        map_running = True

        font_title = pygame.font.SysFont("None", 75)
        font_info = pygame.font.SysFont("None", 50)

        text_title_rendered = font_title.render("Ray Casting engine", True, (255, 255, 255))
        text_info_rendered = font_info.render("Vyberte Mapu", True, (255, 255, 255))

        text_title_pos = text_title_rendered.get_rect(center=(WIDTH / 2, 100))
        text_info_pos = text_info_rendered.get_rect(center=(WIDTH / 2, text_title_pos.bottom + 50))  
        font = pygame.font.SysFont("None", 45)

        map_dir = "maps"  
        map_files = os.listdir(map_dir)

        while map_running:
            self.screen.fill((0, 0, 0))

            self.screen.blit(text_title_rendered, text_title_pos)
            self.screen.blit(text_info_rendered, text_info_pos)

            for i, map_file in enumerate(map_files):
                text_map_rendered = font.render(os.path.splitext(map_file)[0], True, (255, 255, 255))
                text_map_pos = text_map_rendered.get_rect(center=(WIDTH / 2, text_info_pos.bottom + 100 + i * 100)) 
                self.screen.blit(text_map_rendered, text_map_pos)

                if text_map_pos.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255, 0, 0), text_map_pos.inflate(10, 10),2) 

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for i, map_file in enumerate(map_files):
                        text_map_pos = (WIDTH / 2, text_info_pos.bottom + 100 + i * 100)
                        text_map_rendered = font.render(os.path.splitext(map_file)[0], True, (255, 255, 255))
                        text_map_rect = text_map_rendered.get_rect(center=text_map_pos)
                        if text_map_rect.collidepoint(mouse_x, mouse_y):
                            self.current_map = os.path.splitext(map_file)[0]  
                            loaded_map = self.load_map_from_file(os.path.join(map_dir, map_file)) 
                            map_running = False
                            print("Loaded map data:")
                            for row in loaded_map:
                                print(row)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

    def load_map_from_file(self, map_filename):
        try:
            with open(map_filename, 'r') as file:
                lines = file.readlines()
                map_data = [[int(char) for char in line.strip().split(',')] for line in lines]
                engine_map.mini_map = map_data
                return map_data
        except FileNotFoundError:
            print("Chyba: Soubor s mapou nebyl nalezen.")
            return None
        
    def run_menu(self):
        menu_running = True
        while menu_running:
            self.screen.fill((0, 0, 0))
            self.display_menu()
            self.display_texture_menu()  
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (WIDTH / 2 - 100) < mouse_x < (WIDTH / 2 + 100) and 300 < mouse_y < 400:
                        self.current_algorithm = "Linear"
                        self.select_map() 
                        menu_running = False
                    elif (WIDTH / 2 - 100) < mouse_x < (WIDTH / 2 + 100) and 400 < mouse_y < 450:
                        self.current_algorithm = "DDA"
                        self.select_map()  
                        menu_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        self.set_raycasting_algorithm()
        self.new_scene()  

    def get_texture_paths(self):
        texture_dir = "texture"
        texture_paths = []
        for file in os.listdir(texture_dir):
            if file.endswith(".png"):
                texture_paths.append(os.path.join(texture_dir, file))
        return texture_paths

    def run(self):
        self.run_menu() 
        while True:
            self.close()
            self.update_engine()
            self.draw_engine()

if __name__ == "__main__":
    Game().run()
