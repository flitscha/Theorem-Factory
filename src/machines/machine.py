import pygame

from utils import world_to_screen
from settings import TILE_SIZE

class Machine:
    def __init__(self, size=TILE_SIZE, color=(200, 200, 200)):
        self.size = size
        self.color = color

    def update(self):
        pass
    
    def draw(self, screen, camera, grid_x, grid_y):
        screen_x, screen_y = world_to_screen(
            grid_x * self.size,
            grid_y * self.size,
            camera.offset_x,
            camera.offset_y,
            camera.zoom
        )

        pygame.draw.rect(
            screen, 
            self.color, 
            pygame.Rect(screen_x, screen_y, self.size * camera.zoom, self.size * camera.zoom)
        )

