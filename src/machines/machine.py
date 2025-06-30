import pygame

from core.utils import world_to_screen
from config.settings import TILE_SIZE

class Machine:
    def __init__(self, size=(1, 1), color=(200, 200, 200), image=None, rotation=0):
        self.base_size = size # size in grid tiles
        self.color = color
        self.image = image
        self.rotation = rotation
        self.rotated_size = None
        self.update_rotated_size()
        self.rotate_image()
        self.origin = None  # will be set on placement

    def update_rotated_size(self):
        # rotation 0 or 2 means size stays same, 1 or 3 swaps width/height
        if self.rotation % 2 == 1:
            self.rotated_size = (self.base_size[1], self.base_size[0])
        else:
            self.rotated_size = self.base_size

    def rotate_image(self):
        if self.image:
            self.image = pygame.transform.rotate(self.image, -90 * self.rotation)
    
    def update(self):
        pass

    
    def draw(self, screen, camera, grid_x, grid_y):
        screen_x, screen_y = world_to_screen(grid_x * TILE_SIZE, grid_y * TILE_SIZE, camera)

        # draw the image of the machine, if it exists
        if self.image:
            scaled_image = pygame.transform.scale(
                self.image, 
                (int(self.rotated_size[0] * TILE_SIZE * camera.zoom), 
                 int(self.rotated_size[1] * TILE_SIZE * camera.zoom))
            )
            screen.blit(scaled_image, (screen_x, screen_y))
        
        # otherwise draw a rectangle
        else:
            pygame.draw.rect(
                screen, 
                self.color, 
                pygame.Rect(screen_x, screen_y, self.size[0] * TILE_SIZE * camera.zoom, self.size[1] * TILE_SIZE * camera.zoom)
            )

