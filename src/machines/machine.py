import pygame

from utils import world_to_screen
from settings import TILE_SIZE

class Machine:
    def __init__(self, size=1, color=(200, 200, 200), image=None, rotation=0):
        self.size = size # size in grid tiles
        self.color = color
        self.image = image
        self.rotate_image(rotation)

    def update(self):
        pass


    def rotate_image(self, n):
        if self.image:
            self.image = pygame.transform.rotate(self.image, 90 * n)

    
    def draw(self, screen, camera, grid_x, grid_y):
        screen_x, screen_y = world_to_screen(
            grid_x * self.size * TILE_SIZE,
            grid_y * self.size * TILE_SIZE,
            camera.offset_x,
            camera.offset_y,
            camera.zoom
        )

        # draw the image of the machine, if it exists
        if self.image:
            scaled_image = pygame.transform.scale(
                self.image, 
                (int(self.size * TILE_SIZE * camera.zoom), int(self.size * TILE_SIZE * camera.zoom))
            )
            screen.blit(scaled_image, (screen_x, screen_y))
        
        # otherwise draw a rectangle
        else:
            pygame.draw.rect(
                screen, 
                self.color, 
                pygame.Rect(screen_x, screen_y, self.size * TILE_SIZE * camera.zoom, self.size * TILE_SIZE * camera.zoom)
            )

