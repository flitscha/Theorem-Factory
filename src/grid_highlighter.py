import pygame

from settings import TILE_SIZE
from utils import get_grid_coordinates_when_placing_machine, grid_to_screen_coordinates

class GridHighlighter():
    def __init__(self, screen, grid, camera, machine_database):
        self.grid = grid
        self.screen = screen
        self.camera = camera
        self.machine_database = machine_database

        # if you are in build-mode, you can see a preview of the machine you are about to place
        self.active_preview = None # the ID of the machine to preview, or None if no preview is active 

    def start_preview(self, machine_id):
        self.active_preview = machine_id

    def stop_preview(self):
        self.active_preview = None

    def draw(self):
        if self.active_preview:
            data = self.machine_database.get(self.active_preview)
            image = data.image
            size = data.size

            # calculate the grid position
            grid_x, grid_y = get_grid_coordinates_when_placing_machine(self.camera, size)
            screen_x, screen_y = grid_to_screen_coordinates(grid_x, grid_y, self.camera)

            scaled_image = pygame.transform.scale(
                image, 
                (int(size[0] * TILE_SIZE * self.camera.zoom), int(size[1] * TILE_SIZE * self.camera.zoom))
            )

            # Semi-transparent machen (alpha)
            overlay_surface = scaled_image.copy()
            overlay_surface.set_alpha(90)
            self.screen.blit(overlay_surface, (screen_x, screen_y))