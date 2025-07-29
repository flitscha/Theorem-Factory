import pygame

from core.utils import get_mouse_world_pos
from config.constants import TILE_SIZE
from config.settings_manager import settings_manager


class Debug():
    def __init__(self):
        self.font = pygame.font.SysFont(None, 16)

    def draw_coordinates(self, screen, camera):
        mouse_world_x, mouse_world_y = get_mouse_world_pos(camera)
        tile_x = mouse_world_x // TILE_SIZE
        tile_y = mouse_world_y // TILE_SIZE
        coord_text = f"coords: ({int(tile_x)}, {int(tile_y)})"
        coord_surface = self.font.render(coord_text, True, (255, 255, 255))
        screen.blit(coord_surface, (10, 10))
    

    def draw_fps(self, screen, clock):
        fps = clock.get_fps()
        fps_text = f"FPS: {int(fps)}"
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        fps_rect = fps_surface.get_rect(topright=(screen.get_width() - 10, 10))
        screen.blit(fps_surface, fps_rect)


    def draw(self, screen, camera, clock):
        if settings_manager.get("debug.show_coords"):
            self.draw_coordinates(screen, camera)

        if settings_manager.get("debug.show_fps"):
            self.draw_fps(screen, clock)
        